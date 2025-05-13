#!/usr/bin/env python
# coding: utf-8

# ## functions
# 
# New notebook

# In[1]:


import sempy.fabric as fabric 
from datetime import datetime
from notebookutils import mssparkutils
import json
import pytz
import pandas as pd
from pandas import json_normalize
from pyspark.sql.types import StructType, StructField, StringType, IntegerType,TimestampType
from pyspark.sql.functions import col, trim, lower, lit, when, udf, expr
from pyspark.sql import SparkSession,DataFrame
import numpy as np
import warnings
import re
from pyspark.sql import DataFrame


# In[33]:


spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "false")
warnings.filterwarnings("ignore")


# In[34]:


from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("octutils") \
    .getOrCreate()


# In[35]:


def get_executer_alias():
    try:
        executing_user = mssparkutils.env.getUserName()
        at_pos = executing_user.find('@')
        executing_user = executing_user[:at_pos]
    except Exception as e:
        msg = str(e)
        msg = msg.replace('"',"'")
        executing_user = msg = msg.replace("'",'"')
    return executing_user


# In[36]:


def get_modifiedtimestamp():
    try:
        pst_timezone = pytz.timezone('US/Pacific')
        current_time_utc = datetime.now(pytz.utc)
        current_time_pst = current_time_utc.astimezone(pst_timezone)
        current_time_pst = current_time_pst.replace(microsecond=0)
        # Remove timezone info
        current_time_pst = current_time_pst.replace(tzinfo=None)
    except Exception as e:
        current_time_pst = datetime(1900, 1, 1, 0, 0, 0)
    return current_time_pst


# In[37]:


def insert_update_stage_oct(spark_df, oct_table_name, on_name, parameter = "No"):
    tmp_stage = oct_table_name + "_" + "tmp_stage"
    spark_df.write.format("delta").mode("overwrite").saveAsTable(tmp_stage)
    if parameter == "Yes":
        commonquery = f"select commoncolumn from (select a.{on_name} as commoncolumn,a.Name as oldname,b.name as newname,case when a.Name <> 'Unknown'  and b.Name = 'Unknown' then 'No' when a.Name = 'Unknown' and b.Name <> 'Unknown' then 'Yes' when a.Name = 'Unknown' and b.Name = 'Unknown'  then 'Yes' else 'Yes' end deleteflag from {oct_table_name} a join {tmp_stage} b on a.{on_name} = b.{on_name} ) where deleteflag = 'Yes'"
        commonids = spark.sql(commonquery)
        commonids_tuple = tuple(commonids.select("commoncolumn").rdd.map(lambda row: row[0]).collect())
        if len(commonids_tuple) == 0:
            pass
        elif len(commonids_tuple) == 1:
            commonid= commonids_tuple[0]
            delete_query = f"Delete from {oct_table_name} where {on_name} = '{commonid}'"
            spark.sql(delete_query)
        else:
            delete_query = f"Delete from {oct_table_name} where {on_name} in {commonids_tuple}"
            spark.sql(delete_query)
        
        newidsquery = f"select {on_name} as commoncolumn from {tmp_stage} except select {on_name} as commoncolumn from {oct_table_name}"
        newids = spark.sql(newidsquery) 
        newids_tuple = tuple(newids.select("commoncolumn").rdd.map(lambda row: row[0]).collect())
        if len(newids_tuple) == 0:
            pass
        elif len(newids_tuple) == 1:
            newid = newids_tuple[0]
            new_df = spark.sql(f"select * from {tmp_stage} where {on_name} ='{newid}' ")
            new_df.createOrReplaceTempView("newids_table")
            insertquery = f"INSERT INTO {oct_table_name} SELECT * FROM newids_table;"
            spark.sql(insertquery)
        else:
            new_df = spark.sql(f"select * from {tmp_stage} where {on_name} in {newids_tuple} ")
            new_df.createOrReplaceTempView("newids_table")
            insertquery = f"INSERT INTO {oct_table_name} SELECT * FROM newids_table;"
            spark.sql(insertquery)
        
    else:
        commonquery = f"select distinct {on_name} as commoncolumn from {tmp_stage} INTERSECT select distinct {on_name} as commoncolumn from {oct_table_name}"
        commonids = spark.sql(commonquery)
        commonids_tuple = tuple(commonids.select("commoncolumn").rdd.map(lambda row: row[0]).collect())
        if len(commonids_tuple) == 0:
            pass
        elif len(commonids_tuple) == 1:
            commonid= commonids_tuple[0]
            delete_query = f"Delete from {oct_table_name} where {on_name} = '{commonid}'"
            spark.sql(delete_query)
        else:
            delete_query = f"Delete from {oct_table_name} where {on_name} in {commonids_tuple}"
            spark.sql(delete_query)
        
        newidsquery = f"select distinct {on_name} as commoncolumn from {tmp_stage} except select distinct {on_name} as commoncolumn from {oct_table_name}"
        newids = spark.sql(newidsquery) 
        newids_tuple = tuple(newids.select("commoncolumn").rdd.map(lambda row: row[0]).collect())
        if len(newids_tuple) == 0:
            pass
        elif len(newids_tuple) == 1:
            newid = newids_tuple[0]
            new_df = spark.sql(f"select * from {tmp_stage} where {on_name} ='{newid}' ")
            new_df.createOrReplaceTempView("newids_table")
            insertquery = f"INSERT INTO {oct_table_name} SELECT * FROM newids_table;"
            spark.sql(insertquery)
        else:
            new_df = spark.sql(f"select * from {tmp_stage} where {on_name} in {newids_tuple} ")
            new_df.createOrReplaceTempView("newids_table")
            insertquery = f"INSERT INTO {oct_table_name} SELECT * FROM newids_table;"
            spark.sql(insertquery)
        
    return "Operation Completed"


# In[38]:


def get_workspace_name(WorkspaceID,get_all = "No"):
    
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    try:
        WorkspaceID = WorkspaceID.lower()
        client = fabric.FabricRestClient()
        response = client.get(f'https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/')
        metadata = response.json()
        WorkspaceName = metadata.get('displayName','Unknown')
        msg = "{WorkspaceName} workspace name retrieval is successfull "
    except Exception as e:
        WorkspaceName = "Unknown"
        error_response = e.response.json()
        error_code = error_response.get('errorCode', 'No errorCode found')
        error_message = error_response.get('message', 'No message found')
        msg = error_code + "-" + error_message
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    if get_all == "Yes":
        pass
    else:
        schema = StructType([
        StructField("ID", StringType(), True),
        StructField("Name", StringType(), True),
        StructField("Info", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
        ])
        spark_df = spark.createDataFrame([(WorkspaceID,WorkspaceName,msg,Alias,ModifiedTime)], schema)
        info = insert_update_stage_oct(spark_df = spark_df, oct_table_name = "workspacelist", on_name = "ID",parameter = "Yes")
    return (WorkspaceID,WorkspaceName,msg,Alias,ModifiedTime)


# In[39]:


def get_all_workspace_name():
    schema = StructType([
        StructField("ID", StringType(), True),
        StructField("Name", StringType(), True),
        StructField("Info", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
    ])
    workspacelist_df = spark.createDataFrame([], schema)
    get_all = "Yes"
    workspacelist_table = spark.sql("select ID from workspacelist")
    for row in workspacelist_table.collect():
        ID = row['ID']
        WorkspaceID,WorkspaceName,msg,Alias,ModifiedTime =get_workspace_name(WorkspaceID=ID,get_all = get_all)
        new_df = spark.createDataFrame([(WorkspaceID,WorkspaceName,msg,Alias,ModifiedTime)], schema)
        workspacelist_df = workspacelist_df.union(new_df)
    msg = insert_update_stage_oct(spark_df = workspacelist_df, oct_table_name = "workspacelist", on_name = "ID",parameter = "Yes")
    return workspacelist_df


# In[40]:


def get_dataset_name(WorkspaceID,DatasetID,get_all = "No"):
    
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    try:
        WorkspaceID = WorkspaceID.lower()
        client = fabric.FabricRestClient()
        response = client.get(f'https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/items/{DatasetID}')
        metadata = response.json()
        DatasetName = metadata.get('displayName','')
        msg = "{} dataset name is retrieved".format(DatasetName)
    except Exception as e:
        DatasetName = "Unknown"
        error_response = e.response.json()
        error_code = error_response.get('errorCode', 'No errorCode found')
        error_message = error_response.get('message', 'No message found')
        msg = error_code + "-" + error_message
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    if get_all == "Yes":
        pass
    else:
        schema = StructType([
        StructField("WorkspaceID", StringType(), True),
        StructField("ID", StringType(), True),
        StructField("Name", StringType(), True),
        StructField("Info", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
        ])
        spark_df = spark.createDataFrame([(WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime)], schema)
        info = insert_update_stage_oct(spark_df = spark_df, oct_table_name = "datasetlist", on_name = "ID",parameter = "Yes")
    return (WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime)


# In[41]:


def get_all_dataset_name():
    schema = StructType([
        StructField("WorkspaceID", StringType(), True),
        StructField("ID", StringType(), True),
        StructField("Name", StringType(), True),
        StructField("Info", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
        ])
    datasetlist_df = spark.createDataFrame([], schema)
    get_all = "Yes"
    datasetlist_table = spark.sql("select WorkspaceID,ID from datasetlist")
    for row in datasetlist_table.collect():
        WorkspaceID = row['WorkspaceID']
        ID = row['ID']
        WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime =get_dataset_name(WorkspaceID=WorkspaceID,DatasetID=ID,get_all = get_all)
        new_df = spark.createDataFrame([(WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime)], schema)
        datasetlist_df = datasetlist_df.union(new_df)
    msg = insert_update_stage_oct(spark_df = datasetlist_df, oct_table_name = "datasetlist", on_name = "ID",parameter = "Yes")
    return datasetlist_df


# In[42]:


def get_lakehouse_name(WorkspaceID,LakehouseID,get_all = "No"):
    
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    try:
        WorkspaceID = WorkspaceID.lower()
        client = fabric.FabricRestClient()
        response = client.get(f'https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/items/{LakehouseID}')
        metadata = response.json()
        LakehouseName = metadata.get('displayName','')
        msg = "{} dataset name is retrieved".format(LakehouseName)
    except Exception as e:
        LakehouseName = "Unknown"
        error_response = e.response.json()
        error_code = error_response.get('errorCode', 'No errorCode found')
        error_message = error_response.get('message', 'No message found')
        msg = error_code + "-" + error_message
        msg = msg.replace('"',"'")
        msg = msg.replace("'",'"')
    if get_all == "Yes":
        pass
    else:
        schema = StructType([
        StructField("WorkspaceID", StringType(), True),
        StructField("ID", StringType(), True),
        StructField("Name", StringType(), True),
        StructField("Info", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
        ])
        spark_df = spark.createDataFrame([(WorkspaceID,LakehouseID,LakehouseName,msg,Alias,ModifiedTime)], schema)
        info = insert_update_stage_oct(spark_df = spark_df, oct_table_name = "datasetlist", on_name = "ID",parameter = "Yes")
    return (WorkspaceID,LakehouseID,LakehouseName,msg,Alias,ModifiedTime)


# In[43]:


def get_all_lakehouse_name():
    schema = StructType([
        StructField("WorkspaceID", StringType(), True),
        StructField("ID", StringType(), True),
        StructField("Name", StringType(), True),
        StructField("Info", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
        ])
    lakehouselist_df = spark.createDataFrame([], schema)
    get_all = "Yes"
    lakehouselist_table = spark.sql("select WorkspaceID,ID from lakehouselist")
    for row in lakehouselist_table.collect():
        WorkspaceID = row['WorkspaceID']
        ID = row['ID']
        WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime = get_lakehouse_name(WorkspaceID = WorkspaceID,LakehouseID =ID ,get_all = get_all)
        new_df = spark.createDataFrame([(WorkspaceID,DatasetID,DatasetName,msg,Alias,ModifiedTime)], schema)
        lakehouselist_df = lakehouselist_df.union(new_df)
    msg = insert_update_stage_oct(spark_df = lakehouselist_df, oct_table_name = "datasetlist", on_name = "ID",parameter = "Yes")
    return lakehouselist_df


# In[44]:


def normalize_path(value):
    if '/Tables/' in value:
        schema = value.replace('/Tables/', '') + "."
    elif '/Tables' in value:
        schema = value.replace('/Tables', 'dbo') + "."
    else:
        schema = ''
    return schema


# In[45]:


def build_path(node_id, parent_map):
    path = []
    while node_id is not None:
        path.insert(0, node_id)
        node_id = parent_map.get(node_id)
    return ">".join(path)


# In[46]:


def process_shortcuts():
    df = spark.sql("""SELECT Initial_Path,
                            CASE
                            WHEN source_path LIKE '%https://msit-onelake.dfs.fabric.microsoft.com/nan/nan/nan%' THEN NULL
                            ELSE source_path
                            END AS SourcePath
                    FROM oct_shortcuts_stage""")
    parent_map = dict(df.rdd.map(lambda row: (row["Initial_Path"], row["SourcePath"])).collect())

    # Perform recursive resolution in Python
    path_data = [(key, build_path(key, parent_map)) for key in parent_map.keys()]
    path_df = spark.createDataFrame(path_data, ["Initial_Path", "path"])
    df_with_path = df.join(path_df, on="Initial_Path", how="left")

    df_final = df_with_path.withColumn(
        "Final_Source_Path",
        expr("""
            CASE
                WHEN INSTR(path, '>') > 0 THEN SUBSTRING(path, LENGTH(path) - INSTR(REVERSE(path), '>') + 2)
                ELSE path
            END
        """)
    )
    df_final.createOrReplaceTempView("Final_Source_path_Extraction_view")

    final = spark.sql(""" 
        create or replace table oct_shortcuts as
        select a.initial_workspace_id as InitialWorkspaceID,
                a.initial_lakehouse_id as InitialLakehouseID,
                l.Name as InitialLakehouseName,
                concat("https://msit.powerbi.com/groups/",a.initial_workspace_id,"lakehouses/",a.initial_lakehouse_id,"?experience=power-bi") as InitialLakehouseLink,
                a.Initial_Path,
                a.shortcutName as Initial_Shortcut_Name,
                split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[0] AS FinalSourceWorkspaceID,
                split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[1] AS FinalSourceLakehouseID,
                fl.Name as FinalSourceLakehouseName,
                concat("https://msit.powerbi.com/groups/",split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[0],"lakehouses/",split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[1],"?experience=power-bi") as FinalSourceLakehouseLink,
                b.Final_Source_Path,
                case when a.initial_adls_path <> "nannan" then a.initial_adls_path
                        when a.initial_adls_path == "nannan" and c.initial_adls_path <> "nannan" then c.initial_adls_path
                        when a.initial_adls_path == "nannan" and c.initial_adls_path == "nannan" then Null
                        else "Failed Extraction"
                        end as Source_ADLS_Path,
                case when d.Lakehouse_ID is null then "Yes" else "No" end as OSOTLakehouseFlag,
                d.Lakehouse_Type as SourceLakehouseType,
                d.`Area/Domain` as Source_Area_Domain,
                a.Alias,
                a.ModifiedTime
        from oct_shortcuts_stage a 
        join Final_Source_path_Extraction_view b on a.initial_path = b.Initial_Path
        left join oct_shortcuts_stage c on b.Final_Source_Path = c.initial_path
        left join delta.`abfss://ed6737e8-6e3a-4d64-ac9c-3441eec71500@msit-onelake.dfs.fabric.microsoft.com/1df68066-3cfa-44a9-86fe-16135cd86ae8/Tables/OSOT_Lakehouses` d on lcase(trim(split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[1])) = lcase(trim(d.Lakehouse_ID))
        left join lakehouselist l on lcase(trim(l.ID)) = lcase(trim(a.initial_lakehouse_id))  
        left join lakehouselist fl on lcase(trim(fl.ID))  = lcase(trim(split(regexp_replace(b.Final_Source_Path, '^https://msit-onelake\.dfs\.fabric\.microsoft\.com/', ''), '/')[1]))
    """)   
    return "Operation Completed"


# In[47]:


def get_lakehouse_shortcuts(WorkspaceID, LakehouseID, memorylakehouseset,get_all = "No"):
    
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    shortcuts = pd.DataFrame(columns=[
        'initial_workspace_id', 'initial_lakehouse_id','ShortcutName', 'initial_path', 'initial_adls_path',
        'source_workspace_id', 'source_lakehouse_id', 'source_path','Alias','ModifiedTime'
    ])
    errors = pd.DataFrame(columns=['Workspace_ID', 'Item_Type', 'Item_ID', "Error_Message",'Alias','ModifiedTime'])

    try:
        client = fabric.FabricRestClient()
        response = client.get(f"https://api.fabric.microsoft.com/v1/workspaces/{WorkspaceID}/items/{LakehouseID}/shortcuts")
        json_data = response.json().get("value", [])
    except Exception as e:
        errors.loc[len(errors)] = [WorkspaceID, 'lakehouse', LakehouseID, str(e),Alias,ModifiedTime]
        memorylakehouseset.add(LakehouseID)
        return shortcuts, errors, memorylakehouseset

    if json_data and (LakehouseID not in memorylakehouseset):
        try:

            shortcuts_stage = pd.DataFrame(json_data)
            shortcuts_stage["Workspace_ID"] = WorkspaceID
            shortcuts_stage["Lakehouse_ID"] = LakehouseID
        
            shortcuts_stage = shortcuts_stage.drop('target', axis=1).join(json_normalize(shortcuts_stage['target']))            
           
            required_columns = [
                "oneLake.itemId", "oneLake.path", "oneLake.workspaceId",
                "adlsGen2.connectionId", "adlsGen2.location", "adlsGen2.subpath"
            ]
            for col in required_columns:
                if col not in shortcuts_stage.columns:
                    shortcuts_stage[col] = np.nan
            
            shortcuts_stage.rename(columns={
                'name': 'Shortcut_Name',
                'path': 'Shortcut_Path',
                'type': "Shortcut_Type",
                "oneLake.itemId": "oneLake_LakehouseId",
                "oneLake.path": "oneLake_path",
                "oneLake.workspaceId": "oneLake_workspaceId",
                "adlsGen2.connectionId": "adlsGen2_ConnectionId",
                "adlsGen2.location": "adlsGen2_Location",
                "adlsGen2.subpath": "adlsGen2_Subpath"
            }, inplace=True)

            shortcuts_stage = shortcuts_stage[[
                "Workspace_ID", "Lakehouse_ID", "Shortcut_Name", "Shortcut_Path",
                "Shortcut_Type", "oneLake_workspaceId", "oneLake_LakehouseId",
                "oneLake_path", "adlsGen2_Location", "adlsGen2_Subpath", "adlsGen2_ConnectionId"
            ]].astype(str)

            shortcuts['initial_workspace_id'] = shortcuts_stage['Workspace_ID']
            shortcuts['initial_lakehouse_id'] = shortcuts_stage['Lakehouse_ID']
            shortcuts['source_workspace_id'] = shortcuts_stage['oneLake_workspaceId']
            shortcuts['source_lakehouse_id'] = shortcuts_stage['oneLake_LakehouseId']
            
            shortcuts["initial_path"] = (
                "https://msit-onelake.dfs.fabric.microsoft.com/" +
                shortcuts_stage["Workspace_ID"] + "/" +
                shortcuts_stage["Lakehouse_ID"] + shortcuts_stage["Shortcut_Path"] + "/" +
                shortcuts_stage["Shortcut_Name"]
            )
            shortcuts["initial_path"] = shortcuts["initial_path"].astype(str)
       
            shortcuts["source_path"] = (
                "https://msit-onelake.dfs.fabric.microsoft.com/" +
                shortcuts_stage["oneLake_workspaceId"] + "/" +
                shortcuts_stage["oneLake_LakehouseId"] + "/" +
                shortcuts_stage["oneLake_path"]
            )
            shortcuts["source_path"] = shortcuts["source_path"].astype(str)

            shortcuts["initial_adls_path"] = shortcuts_stage["adlsGen2_Location"] + shortcuts_stage["adlsGen2_Subpath"]
    
            shortcuts['ShortcutName']  = shortcuts_stage['Shortcut_Path'].apply(normalize_path) + shortcuts_stage['Shortcut_Name']
            shortcuts['Alias'] = Alias
            shortcuts['ModifiedTime'] = ModifiedTime

           
            oneLake_shortcuts = shortcuts[['source_workspace_id', 'source_lakehouse_id']].drop_duplicates()
            oneLake_shortcuts = oneLake_shortcuts[oneLake_shortcuts['source_lakehouse_id'].notnull()]
            memorylakehouseset.add(LakehouseID)
            
            for idx, row in oneLake_shortcuts.iterrows():
                source_workspace_id = row['source_workspace_id']
                source_lakehouse_id = row['source_lakehouse_id']
                if source_lakehouse_id == 'nan' or source_workspace_id == 'nan':
                    continue
                elif source_lakehouse_id in memorylakehouseset:
                    continue
                else:
                    try:
                        get_workspace_name(WorkspaceID =source_workspace_id,get_all = "No")
                        get_lakehouse_name(WorkspaceID =source_workspace_id,LakehouseID = source_lakehouse_id,get_all = "No")
                        nested_shortcuts, nested_errors, memorylakehouseset = get_lakehouse_shortcuts(
                            WorkspaceID=source_workspace_id,
                            LakehouseID=source_lakehouse_id,
                            memorylakehouseset=memorylakehouseset,
                            get_all = get_all
                        )
                        memorylakehouseset.add(source_lakehouse_id)
                        shortcuts = pd.concat([shortcuts, nested_shortcuts], ignore_index=True)
                        errors = pd.concat([errors, nested_errors], ignore_index=True)
                    except Exception as e:
                        errors.loc[len(errors)] = [source_workspace_id, 'lakehouse', source_lakehouse_id, str(e), Alias, ModifiedTime]

        except Exception as e:
            errors.loc[len(errors)] = [WorkspaceID, 'lakehouse', LakehouseID, str(e),Alias, ModifiedTime] 
        shortcuts = shortcuts.applymap(lambda x: x.lower() if isinstance(x, str) else x) 
        shortcuts = shortcuts.drop_duplicates()
    if get_all == "Yes":
        pass
    else: 
        schema = StructType([
            StructField("initial_workspace_id", StringType(), True),
            StructField("initial_lakehouse_id", StringType(), True),
            StructField("ShortcutName", StringType(), True),
            StructField("initial_path", StringType(), True),
            StructField("initial_adls_path", StringType(), True),
            StructField("source_workspace_id", StringType(), True),
            StructField("source_lakehouse_id", StringType(), True),
            StructField("source_path", StringType(), True),
            StructField("Alias", StringType(), True),
            StructField("ModifiedTime", TimestampType(), True)
        ])
        error_schema =  StructType([
            StructField("Workspace_ID", StringType(), True),
            StructField("Item_Type", StringType(), True),
            StructField("Item_ID", StringType(), True),
            StructField("Error_Message", StringType(), True),
            StructField("Alias", StringType(), True),
            StructField("ModifiedTime", TimestampType(), True)
        ])
        spark_df = spark.createDataFrame(shortcuts,schema)
        errors_df = spark.createDataFrame(errors,error_schema)
        msg = insert_update_stage_oct(spark_df = spark_df, oct_table_name = "oct_shortcuts_stage" , on_name = "initial_lakehouse_id", parameter = "No")
        error_msg = insert_update_stage_oct(spark_df = errors_df, oct_table_name = "oct_errors" , on_name = "Item_ID", parameter = "No")
        process_shortcuts() 
    return shortcuts, errors, memorylakehouseset


# In[48]:


def get_all_lakehouse_shortcuts():
    schema = StructType([
        StructField("initial_workspace_id", StringType(), True),
        StructField("initial_lakehouse_id", StringType(), True),
        StructField("ShortcutName", StringType(), True),
        StructField("initial_path", StringType(), True),
        StructField("initial_adls_path", StringType(), True),
        StructField("source_workspace_id", StringType(), True),
        StructField("source_lakehouse_id", StringType(), True),
        StructField("source_path", StringType(), True),
        StructField("Alias", StringType(), True),
        StructField("ModifiedTime", TimestampType(), True)
        ])
    error_schema =  StructType([
            StructField("Workspace_ID", StringType(), True),
            StructField("Item_Type", StringType(), True),
            StructField("Item_ID", StringType(), True),
            StructField("Error_Message", StringType(), True),
            StructField("Alias", StringType(), True),
            StructField("ModifiedTime", TimestampType(), True)
        ])
    get_all = "Yes"
    memorylakehouseset = set()
    spark_shortcuts = spark.createDataFrame([],schema)
    spark_errors = spark.createDataFrame([],error_schema)
    lakehouselist_table = spark.sql("select WorkspaceID,ID from lakehouselist")
    for row in lakehouselist_table.collect():
        WorkspaceID = row['WorkspaceID']
        ID = row['ID']
        shortcuts_stage, errors_stage, memorylakehouseset  = get_lakehouse_shortcuts(WorkspaceID=WorkspaceID , LakehouseID = ID, memorylakehouseset = memorylakehouseset,get_all = get_all)
        spark_shortcuts_stage = spark.createDataFrame(shortcuts_stage,schema)
        spark_shortcuts = spark_shortcuts.union(spark_shortcuts_stage)
        spark_errors_stage= spark.createDataFrame(errors_stage,error_schema)
        spark_errors = spark_errors.union(spark_errors_stage)
    msg = insert_update_stage_oct(spark_df = spark_shortcuts, oct_table_name = "oct_shortcuts_stage" , on_name = "initial_lakehouse_id", parameter = "No")
    error_msg = insert_update_stage_oct(spark_df = spark_errors, oct_table_name = "oct_errors" , on_name = "Item_ID", parameter = "No")
    process_shortcuts() 
    return spark_shortcuts,spark_errors,memorylakehouseset


# In[49]:


def get_tmsl(Workspace,Dataset):
    tmsl_script = fabric.get_tmsl(Dataset,Workspace)
    tmsl_dict = json.loads(tmsl_script)
    return tmsl_dict


# In[50]:


def extract_right_of_dot(s):
    if "." in s:
        newstring = s.split(".", 1)[1]
    else:
        newstring = s
    return newstring


# In[51]:


def clean_text(text):
    new_string = text.replace("[", "")
    new_string = new_string.replace("]", "")
    new_string = new_string.split('#')[0].strip()
    new_string = new_string.split(')')[0].strip()
    return new_string


# In[52]:


def get_dataset_lineage(WorkspaceID,DatasetID,get_all = "No"):
    
    tables_df =  pd.DataFrame(columns = ['Workspace_ID','Dataset_ID','Mode','Source_Type','Expression',"Table_Name","Source_Table_Name","Alias","ModifiedTime"])
    expressions_df =  pd.DataFrame(columns = ['Workspace_ID','Dataset_ID',"Name","Expression","Alias","ModifiedTime"])
    columns_df = pd.DataFrame(columns = ['Workspace_ID','Dataset_ID',"Table_Name","Column_Name","Data_Type","Alias","ModifiedTime"])
    measures_df = pd.DataFrame(columns = ['Workspace_ID','Dataset_ID',"Table_Name","Measure_Name","Expression","Description","Format","Alias","ModifiedTime"])
    relationships_df = pd.DataFrame(columns = ['WorkspaceID','DatasetID','Name', 'FromTable', 'FromColumn', 'ToTable', 'ToColumn', 'State','CrossFilteringBehavior','SecurityFilteringBehavior', 'Active','ToCardinality', 'RelationshipModifiedTime', 'RefreshedTime',"Alias","ModifiedTime"])
    model_df = pd.DataFrame(columns = ['WorkspaceID','DatasetID','DatasetName','createdTimestamp',"Last_Update","Last_Schema_Update","Last_Processed","Alias","ModifiedTime"])
    roles_df = pd.DataFrame(columns = ['WorkspaceID','DatasetID',"RoleName","RoleModelPermission","RoleModifiedTime",'TableName',"TableFilterExpression","TablemodifiedTime","Alias","ModifiedTime"])
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    try: 
        tmsl = get_tmsl(Workspace = WorkspaceID,Dataset = DatasetID)
        model_name = tmsl.get('name','Unknown') 
        model_createdTimestamp = tmsl.get('createdTimestamp','')
        model_last_update = tmsl.get('lastUpdate','')
        model_last_schema_update = tmsl.get('lastSchemaUpdate','')
        model_last_processed = tmsl.get('lastProcessed','')
        model_df.loc[len(model_df)+1] = [WorkspaceID,DatasetID,model_name,model_createdTimestamp,model_last_update,model_last_schema_update,model_last_processed,Alias,ModifiedTime]
        model = tmsl.get('model',{}) 
        relationships = model.get('relationships',[])
        for relindex in range(len(relationships)):
            relationship = relationships[relindex]
            RelationshipName = relationship.get('name','')
            fromTable = relationship.get('fromTable','')
            fromColumn = relationship.get('fromColumn','')
            toTable = relationship.get('toTable','')
            toColumn = relationship.get('toColumn','')
            state = relationship.get('state','')
            crossFilteringBehavior = relationship.get('crossFilteringBehavior','OneDirection')
            SecurityFilteringBehavior = relationship.get('securityFilteringBehavior','OneDirection')
            Active = relationship.get('isActive','true')
            toCardinality = relationship.get('toCardinality','One') 
            modifiedTime = relationship.get('modifiedTime','')
            refreshedTime = relationship.get('refreshedTime','')
            relationships_df.loc[len(relationships_df)+1] = [WorkspaceID,DatasetID,RelationshipName,fromTable,fromColumn,toTable,toColumn,state,crossFilteringBehavior,SecurityFilteringBehavior,Active,toCardinality,modifiedTime,refreshedTime,Alias,ModifiedTime]
        
        roles = model.get('roles',[])
        for roleindex in range(len(roles)):
            role = roles[roleindex]
            rolename = role.get('name','Unknown')
            rolemodelpermission = role.get('modelPermission','Unknown')
            rolemodifiedTime= role.get('modifiedTime','Unknown')
            rolemembers = role.get('members',[])
            tablePermissions = role.get('tablePermissions',[])
            
            if len(tablePermissions)>0:
                for tablepermissionindex in range(len(tablePermissions)):
                    tablepermissionname = tablePermissions[tablepermissionindex].get('name','')
                    tablepermissionfilterExpression = tablePermissions[tablepermissionindex].get('filterExpression','')
                    tablepermissionmodifiedTime = tablePermissions[tablepermissionindex].get('modifiedTime','')
                roles_df.loc[len(roles_df)+1] = [WorkspaceID,DatasetID,rolename,rolemodelpermission,rolemodifiedTime,tablepermissionname,tablepermissionfilterExpression,tablepermissionmodifiedTime,Alias,ModifiedTime]
            else:
                roles_df.loc[len(roles_df)+1] = [WorkspaceID,DatasetID,rolename,rolemodelpermission,rolemodifiedTime,"Not Applicable","Not Applicable","Not Applicable",Alias,ModifiedTime]
        
        tables = model.get('tables',"Not Present") 

        if tables != "Not Present":
            for index in range(len(tables)):
                table_name = tables[index]["name"] if "name" in tables[index] else "Not Present"
                partitions = tables[index]["partitions"][0] if "partitions" in tables[index] else "Not Present"
                if partitions != "Not Present":
                    mode = partitions["mode"] if "mode" in partitions else "Default"
                    source = partitions["source"] if "source" in partitions else "Not Present"
                    if source != "Not Present":
                        expression = source["expression"] if "expression" in source else "Not Present"
                        expression_type = source["type"] if "type" in source else "Not Present"
                        if expression_type == "calculated":
                            source_table_name = "Calculated in model"
                            source_type = "Power BI/Semantic Model"
                        elif "entityName" in source:
                            source_type = "Microsoft Fabric"
                            source_table_name = source["schemaName"] + '.' + source["entityName"] if "schemaName" in source else source["entityName"]  
                            expression = source["expressionSource"] if "expressionSource" in source else "Not Present"
                        elif 'Sql.Database' in expression:
                            source_type = "SQL Server Database"
                            if 'Item=\"' in expression:
                                if 'Schema=\"' in expression:
                                    source_table_name = expression.split('Schema=\"')[1].split('"')[0] + '.' + expression.split('Item=\"')[1].split('"')[0]
                                else:
                                    source_table_name = expression.split('Item=\"')[1].split('"')[0]
                            elif 'Query=\"' in expression:
                                pattern1 = r'(?<=\bFROM)\s+(\w+\S*)'
                                pattern2 = r'(?<=\bJOIN)\s+(\w+\S*)'
                                pattern3 = r'(delta\.\s+)(\S+)+'
                                pattern4 = r'(parquet\.\s+)(\S+)+'
                                pattern5 = r'(?<=\bfrom)\s+(\[\w+\S*)'
                                pattern6 = r'(?<=\bjoin)\s+(\[\w+\S*)'
                                Query = expression.split('Query=\"')[1].split('"]')[0]
                                pattern_from = re.findall(pattern1, Query, re.IGNORECASE)
                                pattern_join = re.findall(pattern2, Query, re.IGNORECASE)
                                pattern_delta = re.findall(pattern3, Query, re.IGNORECASE)
                                pattern_parquet = re.findall(pattern4, Query, re.IGNORECASE)
                                pattern_from_brace = re.findall(pattern5, Query, re.IGNORECASE)
                                pattern_join_brace = re.findall(pattern6, Query, re.IGNORECASE)
                                source_table_name_list = pattern_from + pattern_join + pattern_delta + pattern_parquet + pattern_from_brace + pattern_join_brace
                                source_table_name = [clean_text(s) for s in source_table_name_list]
                            elif 'Navigation = Source{[Schema = \"' in expression:
                                schema_name = expression.split('Navigation = Source{[Schema = \"')[1].split('"')[0]
                                if 'Item = \"' in expression: 
                                    source_table_name = expression.split('Item = \"')[1].split('"')[0]
                                    source_table_name = source_table_name = schema_name + "." + source_table_name
                                else:
                                    source_table_name = "Item not found"
                            else:
                                source_table_name = "Not Found"
                        elif 'StaticTable' in expression:
                            source_table_name = 'StaticTable'
                            source_type = 'StaticTable'
                        elif 'Row(\"' in expression:
                            source_table_name = 'StaticTable'
                            source_type = 'StaticTable'
                        elif 'Navigation = Source{[Name = \"' in expression:
                            source_table_name = expression.split('Navigation = Source{[Name = \"')[1].split('"')[0]
                            source_type = "Azure" if 'AzureStorage.DataLake' in expression else "Naviagation type Not Defined in code"
                        elif 'Navigation = Source{[Name=\"' in expression:
                            source_table_name = expression.split('Navigation = Source{[Name=\"')[1].split('"')[0]
                            source_type = "Azure" if 'AzureStorage.DataLake' in expression else "Naviagation type Not Defined in code"   
                        elif 'Json.Document(Binary.Decompress(Binary.FromText(\"' in expression:
                            source_table_name = expression.split('Json.Document(Binary.Decompress(Binary.FromText(\"')[1].split('"')[0]
                            source_type = "binary Json Document" if 'Json.Document(Binary' in expression else "Json type Not Defined in code"
                        elif 'Excel.Workbook(File.Contents(\"' in expression:
                            source_table_name = expression.split('Excel.Workbook(File.Contents(\"')[1].split('"')[0]
                            source_type = "Excel Workbook" if 'Excel.Workbook(File.Contents(\"' in expression else "Excel Workbook type Not Defined in code"
                        elif 'Excel.Workbook(Web.Contents(\"' in expression:
                            source_table_name = expression.split('Excel.Workbook(Web.Contents(\"')[1].split('"')[0]
                            source_type = "Excel Workbook" if 'Excel.Workbook(Web.Contents(\"' in expression else "Excel Workbook type Not Defined in code"
                        elif 'Csv.Document(Web.Contents(\"' in expression:
                            source_table_name = expression.split('Csv.Document(Web.Contents(\"')[1].split('"')[0]
                            source_type = "Csv Document" if 'Csv.Document(Web.Contents(\"' in expression else "CSV Document type Not Defined in code"
                        elif 'Source = DateTime.LocalNow()' in expression:
                            source_table_name = 'Calculated DateTime function'
                            source_type = "Calculated Datetime" if 'Source = DateTime.LocalNow()' in expression else "datetime type Not Defined in code"
                        elif 'Source = AzureStorage.DataLake(\"' in expression:
                            source_table_name = expression.split('Source = AzureStorage.DataLake(\"')[1].split('"')[0]
                            source_type = "AzureStorage DataLake" if 'Source = AzureStorage.DataLake(\"' in expression else "AzureStorage DataLake type Not Defined in code"
                        elif 'SharePoint.Tables(\"' in expression:
                            source_table_name = expression.split('SharePoint.Tables(\"')[1].split('"')[0]
                            source_type = "SharePoint" if 'SharePoint.Tables(\"' in expression else "Sharepoint type Not Defined in code"
                        elif 'SharePoint.Files(\"' in expression:
                            source_table_name = expression.split('SharePoint.Files(\"')[1].split('"')[0]
                            source_type = "SharePoint" if 'SharePoint.Files(\"' in expression else "Sharepoint type Not Defined in code"
                        elif 'Databricks.Catalogs(' in expression:
                            try:
                                source_table_name = re.findall(r'Name="(.*?)",Kind="Table"', expression)
                                source_table_name = source_table_name[0]
                                source_type = "Azure Databricks"
                            except Exception as e:
                                source_table_name = str(e)
                                source_type = "Azure Databricks"
                        elif 'Table.Combine({' in expression:
                            source_table_name = "Calculated in model"
                            source_type = "Table Combine"
                        elif 'Table.FromRows(' in expression:
                            source_table_name = "StaticTable"
                            source_type = "StaticTable"
                        elif expression_type == "calculationGroup":
                            source_table_name = "calculationGroup"
                            source_type == expression_type
                        elif 'AnalysisServices.Database' in expression:
                            source_table_name = 'Out of Scope'
                            source_type = 'Out of scope'
                        else:
                            source_type = "Notdefined"
                            source_table_name = "Notdefined"
                        if isinstance(source_table_name, list):
                            for stname in source_table_name:
                                #Source_Table_Name_wo_Schema = extract_right_of_dot(s=stname)
                                tables_df.loc[len(tables_df)+1] = [WorkspaceID,DatasetID,mode,source_type,expression,table_name,stname,Alias,ModifiedTime]
                        else:
                            #Source_Table_Name_wo_Schema = extract_right_of_dot(s=source_table_name)
                            tables_df.loc[len(tables_df)+1] = [WorkspaceID,DatasetID,mode,source_type,expression,table_name,source_table_name,Alias,ModifiedTime]

                
                if 'columns' in tables[index].keys():
                    columns = tables[index]["columns"]
                    for colindex in range(len(columns)):
                        column_name = columns[colindex]["name"] if "name" in columns[colindex] else "Not Present"
                        column_datatype = columns[colindex]["dataType"] if "dataType" in columns[colindex] else "Not Present"
                        columns_df.loc[len(columns_df)+1] = [WorkspaceID,DatasetID,table_name,column_name,column_datatype,Alias,ModifiedTime]
        
                
                if "measures" in tables[index].keys():
                    measures = tables[index]["measures"]
                    for measureindex in range(len(measures)):
                        measure_name = measures[measureindex]["name"] if "name" in measures[measureindex] else "Not Present"
                        measure_expression = measures[measureindex]["expression"] if "expression" in measures[measureindex] else "Not Present"
                        measure_description = measures[measureindex]["description"] if "description" in measures[measureindex] else ""
                        measure_format = measures[measureindex]["formatString"] if "formatString" in measures[measureindex] else ""
                        measures_df.loc[len(measures_df)+1] = [WorkspaceID,DatasetID,table_name,measure_name,measure_expression,measure_description,measure_format,Alias,ModifiedTime]
        
        express = model.get("expressions",[])
        if express:
            for index in range(len(express)):
                expression_name = express[index]["name"]
                expression = express[index]["expression"]
                expressions_df.loc[len(expressions_df)+1] = [WorkspaceID,DatasetID,expression_name,expression,Alias,ModifiedTime]
        
        if get_all == "Yes":
            pass
        else:
            schema_tables = StructType([
                StructField("Workspace_ID", StringType(), True),   
                StructField("Dataset_ID", StringType(), True),    
                StructField("Mode", StringType(), True),
                StructField("Source_Type", StringType(), True), 
                StructField("Expression", StringType(), True), 
                StructField("Table_Name", StringType(), True), 
                StructField("Source_Table_Name", StringType(), True), 
                StructField("Alias", StringType(), True), 
                StructField("ModifiedTime", TimestampType(), True)
            ])
            schema_expressions = StructType([
                    StructField("Workspace_ID", StringType(), True),   
                    StructField("Dataset_ID", StringType(), True),    
                    StructField("Name", StringType(), True),
                    StructField("Expression", StringType(), True),
                    StructField("Alias", StringType(), True), 
                    StructField("ModifiedTime", TimestampType(), True)
                ])
            schema_columns = StructType([
                        StructField("Workspace_ID", StringType(), True),   
                        StructField("Dataset_ID", StringType(), True),    
                        StructField("Table_Name", StringType(), True),
                        StructField("Column_Name", StringType(), True),
                        StructField("Data_Type", StringType(), True),       
                        StructField("Alias", StringType(), True), 
                        StructField("ModifiedTime", TimestampType(), True)
                    ])
            schema_measures = StructType([
                    StructField("Workspace_ID", StringType(), True),   
                    StructField("Dataset_ID", StringType(), True),    
                    StructField("Table_Name", StringType(), True),
                    StructField("Measure_Name", StringType(), True),
                    StructField("Expression", StringType(), True),    
                    StructField("Description", StringType(), True),
                    StructField("Format", StringType(), True),
                    StructField("Alias", StringType(), True), 
                    StructField("ModifiedTime", TimestampType(), True)
                ])
            schema_relationships = StructType([
                    StructField("Workspace_ID", StringType(), True),   
                    StructField("DatasetID", StringType(), True),    
                    StructField("Name", StringType(), True),
                    StructField("FromTable", StringType(), True),
                    StructField("FromColumn", StringType(), True),    
                    StructField("ToTable", StringType(), True),
                    StructField("ToColumn", StringType(), True),
                    StructField("State", StringType(), True),
                    StructField("CrossFilteringBehavior", StringType(), True),
                    StructField("SecurityFilteringBehavior", StringType(), True),
                    StructField("Active", StringType(), True),
                    StructField("ToCardinality", StringType(), True),
                    StructField("RelationshipModifiedTime", StringType(), True),
                    StructField("RefreshedTime", StringType(), True),
                    StructField("Alias", StringType(), True), 
                    StructField("ModifiedTime", TimestampType(), True)
                ])
            schema_model = StructType([
                    StructField("Workspace_ID", StringType(), True),   
                    StructField("DatasetID", StringType(), True),    
                    StructField("DatasetName", StringType(), True),
                    StructField("createdTimestamp", StringType(), True),
                    StructField("Last_Update", StringType(), True),    
                    StructField("Last_Schema_Update", StringType(), True),
                    StructField("Last_Processed", StringType(), True),
                    StructField("Alias", StringType(), True), 
                    StructField("ModifiedTime", TimestampType(), True)
                ])
            schema_role = StructType([
                    StructField("Workspace_ID", StringType(), True),   
                    StructField("DatasetID", StringType(), True),    
                    StructField("RoleName", StringType(), True),
                    StructField("RoleModelPermission", StringType(), True),
                    StructField("RoleModifiedTime", StringType(), True),    
                    StructField("TableName", StringType(), True),
                    StructField("TableFilterExpression", StringType(), True),
                    StructField("TablemodifiedTime", StringType(), True),
                    StructField("Alias", StringType(), True), 
                    StructField("ModifiedTime", TimestampType(), True)
                ]) 
            spark_tables = spark.createDataFrame(tables_df,schema_tables)
            spark_expressions = spark.createDataFrame(expressions_df,schema_expressions)
            spark_columns = spark.createDataFrame(columns_df,schema_columns)
            spark_measures = spark.createDataFrame(measures_df,schema_measures)
            spark_relationship = spark.createDataFrame(relationships_df,schema_relationships)
            spark_model = spark.createDataFrame(model_df,schema_model)
            spark_roles = spark.createDataFrame(roles_df,schema_role)
            
            msg = insert_update_stage_oct(spark_df = spark_tables, oct_table_name = "oct_tables" , on_name = "Dataset_ID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_expressions, oct_table_name = "oct_expression" , on_name = "Dataset_ID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_columns, oct_table_name = "oct_column" , on_name = "Dataset_ID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_measures, oct_table_name = "oct_measures" , on_name = "Dataset_ID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_relationship, oct_table_name = "oct_relationship" , on_name = "DatasetID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_model, oct_table_name = "oct_model" , on_name = "DatasetID", parameter = "No")
            msg = insert_update_stage_oct(spark_df = spark_roles, oct_table_name = "oct_roles" , on_name = "DatasetID", parameter = "No")
    except Exception as e:
        error_schema = StructType([
            StructField("Workspace_ID", StringType(), True),
            StructField("Item_Type", StringType(), True),
            StructField("Item_ID", StringType(), True),
            StructField("Error_Message", StringType(), True),
            StructField("Alias", StringType(), True),
            StructField("ModifiedTime", TimestampType(), True)
        ])

        errors_df = spark.createDataFrame([(WorkspaceID, "Dataset", DatasetID, str(e), Alias, ModifiedTime)],error_schema)
        error_msg = insert_update_stage_oct(spark_df = errors_df, oct_table_name = "oct_errors" , on_name = "Item_ID", parameter = "No")
    return (expressions_df,tables_df,columns_df,measures_df,relationships_df,model_df,roles_df)    


# In[53]:


def get_all_dataset_lineage():
    schema_tables = StructType([
                StructField("Workspace_ID", StringType(), True),   
                StructField("Dataset_ID", StringType(), True),    
                StructField("Mode", StringType(), True),
                StructField("Source_Type", StringType(), True), 
                StructField("Expression", StringType(), True), 
                StructField("Table_Name", StringType(), True), 
                StructField("Source_Table_Name", StringType(), True), 
                StructField("Alias", StringType(), True), 
                StructField("ModifiedTime", TimestampType(), True)
            ])
    schema_expressions = StructType([
            StructField("Workspace_ID", StringType(), True),   
            StructField("Dataset_ID", StringType(), True),    
            StructField("Name", StringType(), True),
            StructField("Expression", StringType(), True),
            StructField("Alias", StringType(), True), 
            StructField("ModifiedTime", TimestampType(), True)
        ])
    schema_columns = StructType([
                StructField("Workspace_ID", StringType(), True),   
                StructField("Dataset_ID", StringType(), True),    
                StructField("Table_Name", StringType(), True),
                StructField("Column_Name", StringType(), True),
                StructField("Data_Type", StringType(), True),       
                StructField("Alias", StringType(), True), 
                StructField("ModifiedTime", TimestampType(), True)
            ])
    schema_measures = StructType([
            StructField("Workspace_ID", StringType(), True),   
            StructField("Dataset_ID", StringType(), True),    
            StructField("Table_Name", StringType(), True),
            StructField("Measure_Name", StringType(), True),
            StructField("Expression", StringType(), True),    
            StructField("Description", StringType(), True),
            StructField("Format", StringType(), True),
            StructField("Alias", StringType(), True), 
            StructField("ModifiedTime", TimestampType(), True)
        ])
    schema_relationships = StructType([
            StructField("Workspace_ID", StringType(), True),   
            StructField("DatasetID", StringType(), True),    
            StructField("Name", StringType(), True),
            StructField("FromTable", StringType(), True),
            StructField("FromColumn", StringType(), True),    
            StructField("ToTable", StringType(), True),
            StructField("ToColumn", StringType(), True),
            StructField("State", StringType(), True),
            StructField("CrossFilteringBehavior", StringType(), True),
            StructField("SecurityFilteringBehavior", StringType(), True),
            StructField("Active", StringType(), True),
            StructField("ToCardinality", StringType(), True),
            StructField("RelationshipModifiedTime", StringType(), True),
            StructField("RefreshedTime", StringType(), True),
            StructField("Alias", StringType(), True), 
            StructField("ModifiedTime", TimestampType(), True)
        ])
    schema_model = StructType([
            StructField("Workspace_ID", StringType(), True),   
            StructField("DatasetID", StringType(), True),    
            StructField("DatasetName", StringType(), True),
            StructField("createdTimestamp", StringType(), True),
            StructField("Last_Update", StringType(), True),    
            StructField("Last_Schema_Update", StringType(), True),
            StructField("Last_Processed", StringType(), True),
            StructField("Alias", StringType(), True), 
            StructField("ModifiedTime", TimestampType(), True)
        ])
    schema_role = StructType([
            StructField("Workspace_ID", StringType(), True),   
            StructField("DatasetID", StringType(), True),    
            StructField("RoleName", StringType(), True),
            StructField("RoleModelPermission", StringType(), True),
            StructField("RoleModifiedTime", StringType(), True),    
            StructField("TableName", StringType(), True),
            StructField("TableFilterExpression", StringType(), True),
            StructField("TablemodifiedTime", StringType(), True),
            StructField("Alias", StringType(), True), 
            StructField("ModifiedTime", TimestampType(), True)
        ]) 
    get_all = "Yes"
    memorylakehouseset = set()
    spark_tables = spark.createDataFrame([],schema_tables)
    spark_expressions = spark.createDataFrame([],schema_expressions)
    spark_columns = spark.createDataFrame([],schema_columns)
    spark_measures = spark.createDataFrame([],schema_measures)
    spark_relationship = spark.createDataFrame([],schema_relationships)
    spark_model = spark.createDataFrame([],schema_model)
    spark_roles = spark.createDataFrame([],schema_role)
    datasetlist_table = spark.sql("select WorkspaceID,ID from datasetlist")
    for row in datasetlist_table.collect():
        WorkspaceID = row['WorkspaceID']
        ID = row['ID']
        expressions_df,tables_df,columns_df,measures_df,relationships_df,model_df,roles_df  = get_dataset_lineage(WorkspaceID = WorkspaceID,DatasetID = ID,get_all = get_all)
        spark_tables_stage = spark.createDataFrame(tables_df,schema_tables)
        spark_expressions_stage = spark.createDataFrame(expressions_df,schema_expressions)
        spark_columns_stage = spark.createDataFrame(columns_df,schema_columns)
        spark_measures_stage = spark.createDataFrame(measures_df,schema_measures)
        spark_relationship_stage = spark.createDataFrame(relationships_df,schema_relationships)
        spark_model_stage = spark.createDataFrame(model_df,schema_model)
        spark_roles_stage = spark.createDataFrame(roles_df,schema_role)
        spark_tables = spark_tables.union(spark_tables_stage)
        spark_expressions = spark_expressions.union(spark_expressions_stage)
        spark_columns = spark_columns.union(spark_columns_stage)
        spark_measures = spark_measures.union(spark_measures_stage)
        spark_relationship = spark_relationship.union(spark_relationship_stage)
        spark_model = spark_model.union(spark_model_stage)
        spark_roles = spark_roles.union(spark_roles_stage)

    msg = insert_update_stage_oct(spark_df = spark_tables, oct_table_name = "oct_tables" , on_name = "Dataset_ID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_expressions, oct_table_name = "oct_expression" , on_name = "Dataset_ID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_columns, oct_table_name = "oct_column" , on_name = "Dataset_ID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_measures, oct_table_name = "oct_measures" , on_name = "Dataset_ID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_relationship, oct_table_name = "oct_relationship" , on_name = "DatasetID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_model, oct_table_name = "oct_model" , on_name = "DatasetID", parameter = "No")
    msg = insert_update_stage_oct(spark_df = spark_roles, oct_table_name = "oct_roles" , on_name = "DatasetID", parameter = "No")
    return "Operation Completed"


# In[ ]:


def create_datasetlistv1_table():
    ps = spark.read.csv('Files/PowerBIDatasetInfo.csv', header=True)
    ds = spark.sql("select * from datasetlist")
    om = spark.sql("select * from oct_model")
    ps = ps.alias("ps")
    ds = ds.alias("ds")
    om = om.alias("om")
    df = ds.join(ps, col("ds.ID") == col("ps.DatasetId"), "left") \
           .join(om, col("om.DatasetID") == col("ds.ID"), "left")
    df = df.select(
        col("ds.WorkspaceID").alias("WorkspaceID"),
        col("ds.ID").alias("DatasetID"),
        col("ds.Name").alias("Name"),
        col("ds.Alias").alias("ExecuterAlias"),
        col("ds.Info").alias("Info"),
        col("ds.ModifiedTime").alias("ModifiedTime"),
        col("ps.ConfiguredBy").alias("ConfiguredBy"),
        col("ps.IsRefreshable").alias("IsRefreshable"), 
        col("om.createdTimestamp").alias("createdTimeStamp"),
        col("om.Last_Update").alias("LastUpdatedTime"),
        col("om.Last_Schema_Update").alias("LastSchemaUpdateTime"),
        col("om.Last_Processed").alias("LastProcessed")
    )

    df.write.format("delta").mode("overwrite").saveAsTable("datasetlistv1")
    return df


# In[ ]:


def save_factocttable():
    factoct= spark.sql("""create or replace table factoct as 
                            select t.Workspace_ID
                                ,t.Dataset_ID
                                ,t.Mode
                                ,t.Source_Type
                                ,t.Expression
                                ,t.Table_Name
                                ,t.Source_Table_Name
                                ,s.InitialWorkspaceID
                                ,s.InitialLakehouseID
                                ,s.InitialLakehouseName
                                ,s.InitialLakehouseLink
                                ,s.Initial_Path
                                ,s.Initial_Shortcut_Name
                                ,s.FinalSourceWorkspaceID
                                ,s.FinalSourceLakehouseID
                                ,s.FinalSourceLakehouseName
                                ,s.FinalSourceLakehouseLink
                                ,s.Final_Source_Path
                                ,s.Source_ADLS_Path
                                ,s.OSOTLakehouseFlag
                                ,s.SourceLakehouseType
                                ,s.Source_Area_Domain
                                ,t.Alias as ExecutorAlias
                                ,t.ModifiedTime as ExecutorModifiedTIme
                         from oct_tables t 
                         left join oct_parameters p on lcase(trim(t.Dataset_ID)) = lcase(trim(p.DatasetID))
                         left join oct_shortcuts s on lcase(trim(t.Source_Table_Name)) = lcase(trim(s.Initial_Shortcut_Name)) 
                         and lcase(trim(p.LakehouseID)) = lcase(trim(s.InitialLakehouseID))""")
    return factoct


# In[55]:


def run(WorkspaceID,DatasetID,LakehouseWorkspaceID = "NA",LakehouseID = "NA"):
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    get_workspace_name(WorkspaceID = WorkspaceID,get_all = "No")
    get_dataset_name(WorkspaceID = WorkspaceID,DatasetID = DatasetID,get_all = "No")
    expressions_df,tables_df,columns_df,measures_df,relationships_df,model_df,roles_df = get_dataset_lineage(WorkspaceID = WorkspaceID,DatasetID = DatasetID,get_all = "No")
    if LakehouseID == "NA" or LakehouseWorkspaceID == "NA":
        df_parameter = fabric.evaluate_dax(dataset= DatasetID,workspace = WorkspaceID,dax_string = """select [rootlocation] from $SYSTEM.TMSCHEMA_DELTA_TABLE_METADATA_STORAGES""")
        if len(df_parameter)==0:
            LakehouseID = "NA"
            LakehouseWorkspaceID == "NA"
        else:
            df_parameter[['LakehouseWorkspaceID', 'LakehouseID']] = df_parameter['rootlocation'].str.extract(r'^/([^/]+)/([^/]+)/')
            df_parameter = df_parameter[['LakehouseWorkspaceID', 'LakehouseID']].drop_duplicates()
            LakehouseWorkspaceID = df_parameter['LakehouseWorkspaceID'][0]
            LakehouseID = df_parameter['LakehouseID'][0]
    get_workspace_name(WorkspaceID = LakehouseWorkspaceID,get_all = "No")    
    get_lakehouse_name(WorkspaceID = LakehouseWorkspaceID,LakehouseID= LakehouseID,get_all = "No")
    shortcuts_df, errors, memorylakehouseset = get_lakehouse_shortcuts(WorkspaceID = LakehouseWorkspaceID, LakehouseID= LakehouseID , memorylakehouseset = set(),get_all = "No")
    query = f"SELECT count(1) as output FROM oct_parameters WHERE lcase(trim(DatasetID)) = '{DatasetID}'"
    df = spark.sql(query)
    flag = df.select("output").first()[0]
    if flag ==0:
        spark.sql(f"INSERT INTO oct_parameters VALUES ('{WorkspaceID}', '{DatasetID}','{LakehouseWorkspaceID}','{LakehouseID}','{Alias}','{ModifiedTime}')")
    elif flag ==1:
        spark.sql(f"UPDATE oct_parameters SET WorkspaceID = '{WorkspaceID}',LakehouseWorkspaceID = '{LakehouseWorkspaceID}',LakehouseID = '{LakehouseID}',Alias = '{Alias}' , ModifiedTime = '{ModifiedTime}' WHERE lcase(DatasetID) = '{DatasetID}'")
    create_datasetlistv1_table()
    save_factocttable()
    return expressions_df,tables_df,columns_df,measures_df,relationships_df,model_df,roles_df,shortcuts_df


# In[61]:


def run_pipeline():
    spark.sql("delete from oct_errors")
    Alias = get_executer_alias()
    ModifiedTime = get_modifiedtimestamp()
    get_all_dataset_lineage()
    get_all_lakehouse_shortcuts()
    get_all_workspace_name()
    get_all_dataset_name()
    get_all_lakehouse_name()
    datasetlist_spark = spark.sql("select * from datasetlist")
    schema = StructType([StructField("WorkspaceID", StringType(), True),
                         StructField("DatasetID", StringType(), True),
                         StructField("LakehouseWorkspaceID", StringType(), True),
                         StructField("LakehouseID", StringType(), True),
                         StructField("Alias", StringType(), True), 
                         StructField("ModifiedTime", TimestampType(), True)
                         ])
    df_parameters = spark.createDataFrame([], schema)
    for row in datasetlist_spark.collect():
        WorkspaceID = row['WorkspaceID'] 
        DatasetID = row['ID'] 
        df_parameter = fabric.evaluate_dax(dataset= DatasetID,workspace = WorkspaceID,dax_string = """select [rootlocation] from $SYSTEM.TMSCHEMA_DELTA_TABLE_METADATA_STORAGES""")
        if len(df_parameter)==0: 
            df_parameter = spark.createDataFrame([(WorkspaceID, DatasetID,"NA", "NA",Alias,ModifiedTime)], schema)
            df_parameters = df_parameters.union(df_parameter)
        else:
            df_parameter[['LakehouseWorkspaceID', 'LakehouseID']] = df_parameter['rootlocation'].str.extract(r'^/([^/]+)/([^/]+)/')
            df_parameter = df_parameter[['LakehouseWorkspaceID', 'LakehouseID']].drop_duplicates()
            df_parameter['WorkspaceID'] = WorkspaceID
            df_parameter['DatasetID'] = DatasetID
            df_parameter['Alias'] = Alias
            df_parameter['ModifiedTime'] = ModifiedTime
            df_parameter = df_parameter[['WorkspaceID','DatasetID','LakehouseWorkspaceID', 'LakehouseID','Alias','ModifiedTime']]
            df_parameter = spark.createDataFrame(df_parameter)
            df_parameters = df_parameters.union(df_parameter)
    df_parameters.write.format("delta").mode("overwrite").saveAsTable("oct_parameters")
    create_datasetlistv1_table()
    save_factocttable()
    return "Operation Completed"

