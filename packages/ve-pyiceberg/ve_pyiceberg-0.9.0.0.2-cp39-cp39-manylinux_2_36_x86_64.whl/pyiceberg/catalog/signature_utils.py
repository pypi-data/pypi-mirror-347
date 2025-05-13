import datetime
import hashlib
import hmac

from hive_metastore.cloudTtypes import Authentication
from hive_metastore.ttypes import Table

# 定义常量
CHARSET = 'utf-8'
ALGORITHM = 'HMAC-SHA256'
TIME_FORMAT_V4 = '%Y%m%dT%H%M%SZ'
TZ_UTC = datetime.timezone.utc

def sign(region, service, request_date, method_name, parameter_types, args, signed_key):
    auth = args[0]
    version = auth.version
    if version.lower() == "v3":
        return signV3(region, service, request_date, method_name, args, signed_key)
    if version.lower() == "v0" and len(args) == 3 and signed_key is not None:
        return signV0(args[1], args[2], signed_key)

    date = request_date[:8]
    canonical_request = method_name + "\n"
    if len(parameter_types) != len(args):
        raise ValueError(f"parameter types length {len(parameter_types)} doesn't equal to args length {len(args)}!")

    for i in range(1, len(parameter_types)):
        if version.lower() == "v2":
            canonical_request += parameter_types[i].__name__
        else:
            canonical_request += f"{parameter_types[i].__module__}.{parameter_types[i].__name__}"
        canonical_request += "\n"
        if args[i] is None:
            value = 0
        # elif isinstance(args[i], TEnum):
        #     value = args[i].getValue()
        # elif isinstance(args[i], list):
        #     if len(args[i]) > 0 and isinstance(args[i][0], TEnum):
        #         values = [o.getValue() for o in args[i]]
        #         value = hash(tuple(values))
        #     else:
        #         value = hash(tuple(args[i]))
        else:
            value = hash(args[i])
        canonical_request += str(value) + "\n"

    canonical_request += f"auth {version}/{auth.getAccessKeyId()}/{auth.getSessionToken()}/{auth.getRequestDate()}/{auth.getServiceName()}/{auth.getRegion()}"
    if auth.getIdentityId() is not None:
        canonical_request += f"/{auth.getIdentityId()}/{auth.getIdentityType()}"
    canonical_request += "\n"

    credential_scope = f"{date}/{region}/{service}/request"
    print(f"canonicalRequest: {canonical_request}")
    print(f"credentialScope: {credential_scope}")
    string_to_sign = f"HMAC-SHA256\n{request_date}\n{credential_scope}\n{sha256(canonical_request)}"
    return bytes_to_hex(hmac_digest(signed_key, string_to_sign))

def signV0(identity_id, identity_type, signed_key):
    string_to_sign = (identity_id + identity_type).upper()
    return bytes_to_hex(hmac_digest(signed_key, string_to_sign))

def signV3(region, service, request_date, method_name, args, signed_key):
    canonical_request = method_name + str(calc_args_hash_code(method_name, args))
    credential_scope = f"{request_date[:8]}/{region}/{service}/request"
    # 对 canonical_request 进行 UTF-8 编码
    string_to_sign = f"HMAC-SHA256{request_date}{credential_scope}{sha256(canonical_request)}"
    return bytes_to_hex(hmac_digest(signed_key, string_to_sign))

NULL_STRING = "NULL"
BASE_NUM = 1000000000

def to_signed(byte):
    return byte if byte < 128 else byte - 256

def ignore_args_for_compatibility(method_name, index):
    if method_name == "create_table_with_constraints" and index > 3:
        return True
    return False

def calc_args_hash_code(method_name, args) -> int:
    hash_value = 1
    for i, obj in enumerate(args):
        if ignore_args_for_compatibility(method_name, i):
            continue
        target_obj = obj
        if isinstance(obj, Authentication):
            # 这里简单复制，实际需要实现深拷贝
            target_obj = Authentication(obj.version, obj.accessKeyId, obj.sessionToken, obj.requestDate, obj.serviceName, obj.region, obj.identityId, obj.identityType)
            target_obj.signature = ""
        hash_value = calc_hash_code(hash_value, calc_object_hash_code(target_obj))
    return hash_value

def calc_object_hash_code(obj) -> int:
    if obj is None:
        return calc_string_hash_code(NULL_STRING)
    elif hasattr(obj, '_NAMES_TO_VALUES'):
        return calc_string_hash_code(str(obj._NAMES_TO_VALUES.get(obj)))
    elif isinstance(obj, dict):
        if not obj:
            return 1
        hash_codes = []
        for key, value in obj.items():
            hash_code = calc_hash_code(1, calc_object_hash_code(key))
            hash_code = calc_hash_code(hash_code, calc_object_hash_code(value))
            hash_codes.append(hash_code)
        hash_codes.sort()
        return calc_list_hash_code(hash_codes)
    elif isinstance(obj, list):
        if not obj:
            return 1
        hash_codes = [calc_object_hash_code(item) for item in obj]
        hash_codes.sort()
        return calc_list_hash_code(hash_codes)
    elif isinstance(obj, set):
        if not obj:
            return 1
        hash_codes = [calc_object_hash_code(item) for item in obj]
        hash_codes.sort()
        return calc_list_hash_code(hash_codes)
    elif isinstance(obj, float):
        return calc_string_hash_code(str(int(obj * BASE_NUM)))
    elif isinstance(obj, str):
        if not obj:
            return 1
        return calc_string_hash_code(obj)
    elif isinstance(obj, bytes):
        return calc_byte_array_hash_code(obj)
    elif hasattr(obj, '__dict__'):
        return calc_tbase_hash_code(obj)
    elif isinstance(obj, bool):
        return calc_string_hash_code(str(obj).lower())
    else:
        return calc_string_hash_code(str(obj))

def calc_byte_array_hash_code(bytes_data) -> int:
    hash_value = 1
    for b in bytes_data:
        hash_value = calc_hash_code(hash_value, b)
    return hash_value

def calc_string_hash_code(s) -> int:
    hash_value = 1
    for b in s.encode(CHARSET):
        hash_value = calc_hash_code(hash_value, b)
    return hash_value

def calc_list_hash_code(hash_codes) -> int:
    hash_value = 1
    for item in hash_codes:
        hash_value = calc_hash_code(hash_value, item)
    return hash_value

def calc_tbase_hash_code(obj) -> int:
    hash_value = 1
    try:
        for field in obj.__dict__:
            # 过滤掉以 __ 开头的内部变量
           if field.startswith('__'):
               continue
           value = getattr(obj, field)
           if ignore_hash_for_compatibility(obj, field):
               continue
           if value is None:
               continue
           if isinstance(value, str) and not value:
               continue
           if isinstance(value, dict) and not value:
               continue
           if isinstance(value, list) and not value:
               continue
           if isinstance(value, set) and not value:
               continue
           if (isinstance(value, float) and value == 0.0) or \
                   (isinstance(value, bool) and not value) or \
                   (isinstance(value, (int,)) and value == 0):
               continue
           hash_value = calc_hash_code(hash_value, calc_object_hash_code(value))
    except Exception as e:
        print(f"Failed calculate TBase hashcode for {obj}: {e}")
    return hash_value

def ignore_hash_for_compatibility(obj, field_name):
    if isinstance(obj, Table):
        if field_name == "ownerType":
            return True
    return False

def calc_hash_code(hash_value: int, value: int) -> int:
    # return (hash_value << 5) - hash_value + value
    hash_value = to_java_int(hash_value)
    temp = to_java_int(hash_value << 5)
    temp = to_java_int(temp - hash_value)
    return to_java_int(temp + value)

def to_java_int(n: int) -> int:
    n &= 0xFFFFFFFF
    return n if n < 0x80000000 else n - 0x100000000

def generate_signed_key(secret_access_key, date, region, service):
    key = hmac_digest(secret_access_key, date)
    key = hmac_digest(key, region)
    key = hmac_digest(key, service)
    return hmac_digest(key, "request")

def get_current_format_date():
    # return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    utc_timezone = datetime.timezone.utc
    # 获取当前时间
    current_date = datetime.datetime.now(utc_timezone)
    # 格式化时间
    formatted_date = current_date.strftime("%Y%m%dT%H%M%SZ")
    return formatted_date

def hex_string_to_byte_array(s):
    return bytes.fromhex(s)

def hmac_digest(secret_key, message):
    if isinstance(message, str):
        message = message.encode(CHARSET)
    if isinstance(secret_key, str):
        secret_key = secret_key.encode(CHARSET)
    hashmc = hmac.new(secret_key, message, hashlib.sha256).digest()
    return hashmc
        # [struct.unpack('b', bytes([byte]))[0] for byte in hashmc]


def sha256(message):
    if isinstance(message, str):
        message = message.encode(CHARSET)
    return hashlib.sha256(message).hexdigest()

def bytes_to_hex(bytes_data):
    return bytes_data.hex()
