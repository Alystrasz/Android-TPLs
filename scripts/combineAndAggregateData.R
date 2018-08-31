# This function combines all the metrics of different minimal apps into two CSV files:
# One file contains the information of all metrics by run.
# Another file contains the aggregated value (median) of each metric.

combineAndAggregateData <- function (inputFileForMetrics,
                                     inputFileForApkSizes,
                                     inputFileForPermissions,
                                     outputFileForMetrics, 
                                     outputFileForApkSizes,
                                     outputFileForPermissions,
                                     outputFileAllData,
                                     outputFileAllDataByRun)
{
  metrics = read.csv(inputFileForMetrics)
  aggregatedData = aggregate(metrics[,c("Value")], by = list(SdkName = metrics$SdkName, SdkType = metrics$SdkType, Metric = metrics$Metric), FUN=median)
  aggregatedData=aggregatedData[order(aggregatedData$SdkType,aggregatedData$Metric,aggregatedData$SdkName),]
  colnames(aggregatedData) = c("SdkName", "SdkType", "Metric", "Value")
  write.csv(aggregatedData, file = outputFileForMetrics, row.names = FALSE)
  
  apkSizes = read.csv(inputFileForApkSizes)
  apkSizes$Run = NA
  apkSizes$Metric = "APK size"
  apkSizes <- apkSizes[c("SdkName", "SdkType", "Metric", "Run", "Size")]
  colnames(apkSizes) = colnames(metrics)
  write.csv(apkSizes, file = outputFileForApkSizes, row.names = FALSE)
  
  permissions = read.csv(inputFileForPermissions)
  permissions = aggregate(permissions[,c("Permission")], by = list(SdkName = permissions$SdkName, SdkType = permissions$SdkType), FUN=length)
  permissions$Run = NA
  permissions$Metric = "Permissions"
  permissions <- permissions[c("SdkName", "SdkType", "Metric", "Run", "x")]
  colnames(permissions) = colnames(metrics)
  write.csv(permissions, file = outputFileForPermissions, row.names = FALSE)
  
  allDataByRun = rbind(metrics, apkSizes, permissions)
  colnames(allDataByRun) = c("individual","group","variable","sample","value")
  
  allData = rbind(aggregatedData, apkSizes[,c("SdkName", "SdkType", "Metric", "Value")], permissions[,c("SdkName", "SdkType", "Metric", "Value")])
  colnames(allData) = c("individual","group","variable","value")
  
  #Write output dataframe for aggregated metrics
  write.csv(allData, file = outputFileAllData, row.names = FALSE)
  
  #Write output dataframe for metrics by run
  write.csv(allDataByRun, file = outputFileAllDataByRun, row.names = FALSE)
}
