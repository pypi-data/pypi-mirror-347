import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tdsbrondata
from pyspark.sql import functions as F
from pyspark.sql.types import *

def getCurrentData(workspaceName, lakehouseName, schemaName, tableName):
    
    abfss = f"abfss://{workspaceName}@onelake.dfs.fabric.microsoft.com/{lakehouseName}.Lakehouse/Tables/{schemaName}/{tableName}"

    data = tdsbrondata._spark.read.format("delta").load(abfss).filter(
        (F.col("CurrentFlag") == 1) & 
        (F.col("ScdEndDate").isNull())
    )

    return data