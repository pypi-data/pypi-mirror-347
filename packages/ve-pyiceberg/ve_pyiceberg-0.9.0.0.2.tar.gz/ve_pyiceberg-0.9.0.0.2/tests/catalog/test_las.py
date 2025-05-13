import os

import hive_metastore.cloudTtypes
from hive_metastore.cloudTtypes import Authentication
from hive_metastore.ttypes import StorageDescriptor
from pyiceberg.catalog import load_catalog, signature_utils
from pyiceberg.exceptions import NamespaceAlreadyExistsError
from pyiceberg.schema import Schema
from pyiceberg.table import AddSchemaUpdate
from pyiceberg.types import NestedField, StringType, DoubleType, LongType

def test_signature():
    catalog = load_catalog(
        "hive",
        **{
            'type': 'hive',
            "uri": "thrift://180.184.98.233:48869",
            "tos.endpoint": "tos-cn-beijing.volces.com",
            "tos.access-key-id": "AKLTOTh*",
            "tos.secret-access-key": "TVdWbVl6*",
            "tos.region": "cn-beijing",
            "las.enabled": True,
            "las.access-key-id": "AKLTOTh*",
            "las.secret-access-key": "TVdWbVl6*",
            "las.region": "cn-beijing"
        }
    )
    print("hello world")
    method_name = "create_table"
    params = ["create_table"]
    from hive_metastore.ttypes import Table
    from hive_metastore.ttypes import FieldSchema
    from hive_metastore.ttypes import SerDeInfo
    sd = StorageDescriptor(compressed = False)
    print(signature_utils.calc_object_hash_code(sd))
    cols = [FieldSchema(name = 'city', type = 'string', comment = None), FieldSchema(name = 'lat', type = 'double', comment = None), FieldSchema(name = 'long', type = 'double', comment = None)]
    for c in cols:
        if c.name == "city":
            assert signature_utils.calc_object_hash_code(c) == 118819751
        elif c.name == "lat":
            assert signature_utils.calc_object_hash_code(c) == -434215787
        elif c.name == "long":
            assert signature_utils.calc_object_hash_code(c) == -306668426

    serdeInfo = SerDeInfo(name=None, serializationLib = "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe", parameters = None)
    assert signature_utils.calc_object_hash_code(serdeInfo) == 1378284243
    sd = StorageDescriptor(cols = cols,
                           location = "tos://emr-autotest/lasformation/warehouse/zhongqiang_py_iceberg.db/test1",
                           inputFormat = "org.apache.hadoop.mapred.FileInputFormat",
                           outputFormat = "org.apache.hadoop.mapred.FileOutputFormat",
                           compressed = False,
                           numBuckets = 0,
                           serdeInfo = serdeInfo,
                           bucketCols = None,
                           sortCols = None,
                           parameters = None)
    assert signature_utils.calc_object_hash_code(sd) == -287825882
    tbl = Table(tableName = "test1", dbName = "zhongqiang_py_iceberg",
                owner = "bytedance", createTime = 1742478640, lastAccessTime = 1742478640, retention = 0,
                sd =  None,
                partitionKeys = None,
                parameters = {"metadata_location": "tos://emr-autotest/lasformation/warehouse/zhongqiang_py_iceberg.db/test1/metadata/00000-da7647a4-b20d-4cbd-878b-97aca97cc106.metadata.json", "EXTERNAL": "TRUE", "table_type": "ICEBERG"}
                , viewOriginalText = None, viewExpandedText = None, tableType = "EXTERNAL_TABLE", temporary = False
                , ownerType = hive_metastore.cloudTtypes.GeminiPrincipalType.USER
                )
    assert signature_utils.calc_object_hash_code(tbl) == 432969615
    request_date = "20250320T135040Z"
    secret_access_key = "TVdWbVl6*"
    region = "cn-beijing"
    service_name = "catalog_service"
    auth = Authentication("v3",
                          "AKLTOTh*",
                          None,
                          "20250320T135040Z",
                          "catalog_service",
                          "cn-beijing",
                          None,
                          None,
                          None)
    date = request_date[:8]
    signed_key = signature_utils.generate_signed_key(secret_access_key, date, region, service_name)
    assert " ".join(map(str, (to_signed(b) for b in signed_key))) == "14 119 42 -103 -1 34 106 53 115 -120 -114 -65 87 -104 -51 -19 -12 -9 102 -34 110 -11 -116 63 55 -29 8 -105 -74 19 82 24"
    new_args = [auth, tbl]
    auth.signature = signature_utils.sign(region, service_name, auth.requestDate, method_name, ["abc"], new_args, signed_key)
    assert auth.signature == "bc636cefd943f95be8ec66762ce40a887460e99f7bb20539d5fd1b00f6303368"

def to_signed(byte):
    return byte if byte < 128 else byte - 256


def test_load_ctalog():
    catalog = load_catalog(
        "hive",
        **{
            'type': 'hive',
            "uri": "thrift://180.184.98.233:48869",
            "tos.endpoint": "tos-cn-beijing.volces.com",
            "tos.access-key-id": os.getenv("access-key-id"),
            "tos.secret-access-key": os.getenv("secret-key-id"),
            "tos.region": "cn-beijing",
            "las.enabled": True,
            "las.access-key-id": os.getenv("access-key-id"),
            "las.secret-access-key": os.getenv("secret-key-id"),
            "las.region": "cn-beijing",
            "las.catalog-name": "zhongqiang_cat"
        }
    )
    try:
        listTables = catalog.list_tables("zhongqiang_py_iceberg2")
        for table in listTables:
            catalog.drop_table(table)
    except Exception as e:
        print(e)

    catalog.drop_namespace("zhongqiang_py_iceberg2")

    catalog.create_namespace_if_not_exists("zhongqiang_py_iceberg2")
    try:
        catalog.create_namespace("zhongqiang_py_iceberg2")
    except Exception as e:
        assert "@zhongqiang_cat#zhongqiang_py_iceberg2 already exists" in (NamespaceAlreadyExistsError(e)).__str__()

    assert ("zhongqiang_py_iceberg2",) in catalog.list_namespaces()

    assert catalog.table_exists("zhongqiang_py_iceberg2.filter_test_table_iceberg_6") == False

    listTables = catalog.list_tables("zhongqiang_py_iceberg2")

    assert len(listTables) == 0

    #假设我们创建一个简单的表，包含一个名为 'id' 的整数列
    schema = Schema(
        NestedField(field_id= 1, name="city", type=StringType(), required=False),
        NestedField(field_id=2, name="lat",  type=DoubleType(), required=False),
        NestedField(field_id=3, name="long", type=DoubleType(), required=False),
    )
    try:
        catalog.create_table("zhongqiang_py_iceberg3.test2", schema=schema)
    except Exception as e:
        assert "zhongqiang_py_iceberg3" in e.__str__()

    create_tbl = catalog.create_table("zhongqiang_py_iceberg2.test2", schema=schema)
    assert create_tbl._identifier == ("zhongqiang_py_iceberg2", "test2")

    given_table = catalog.load_table("zhongqiang_py_iceberg2.test2")

    assert given_table._identifier == ("zhongqiang_py_iceberg2", "test2")
    new_schema = Schema(
        NestedField(10, "x11", LongType()),
        NestedField(12, "y11", LongType(), doc="comment"),
        NestedField(13, "z11", LongType()),
        NestedField(14, "add11", LongType()),
    )

    # When
    response = given_table.catalog.commit_table(
        given_table,
        updates=(
            AddSchemaUpdate(schema=new_schema, last_column_id=new_schema.highest_field_id),
        ),
        requirements=(),
    )

    given_table = given_table.transaction().set_properties(abc="def").commit_transaction()
    assert given_table.properties == {"abc": "def", "write.parquet.compression-codec": "zstd"}
