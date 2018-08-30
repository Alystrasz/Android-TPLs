# This script reads quality metrics of minimal apps and makes a pairwise comparison between TPLs.
# It applies statistical tests and generates different plots to ease the comparison of different TPLs and each quality metric.

require(ggplot2)
require(data.table)
require(gridExtra)

PATH = "/Experiments/"
source(paste(PATH,"combineAndAggregateData.R", sep = ""))
source(paste(PATH,"computeDifferences.R", sep = ""))
source(paste(PATH,"computeStatisticalTests.R", sep = ""))
source(paste(PATH,"generateBoxplotsByGroup.R", sep = ""))
source(paste(PATH,"generatePlotForDifferencesByGroup.R", sep = ""))

# Constants
OUTPUT_FOLDER = paste(PATH,"results/",sep="")
DATA_FILE_FOR_METRICS = paste(OUTPUT_FOLDER,"metrics.csv", sep="")
OUTPUT_FILE_FOR_METRICS = paste(OUTPUT_FOLDER,"metricsAggregated.csv", sep="")
DATA_FILE_FOR_APKSIZES = paste(OUTPUT_FOLDER,"apkSizes.csv", sep="")
OUTPUT_FILE_FOR_APKSIZES = paste(OUTPUT_FOLDER,"apkSizesNewFormat.csv", sep="")
DATA_FILE_FOR_PERMISSIONS = paste(OUTPUT_FOLDER,"permissions.csv", sep="")
OUTPUT_FILE_FOR_PERMISSIONS = paste(OUTPUT_FOLDER,"permissionsCount.csv", sep="")
OUTPUT_FILE_ALL_DATA = paste(OUTPUT_FOLDER,"allData.csv", sep="")
OUTPUT_FILE_ALL_DATA_BY_RUN = paste(OUTPUT_FOLDER,"allDataByRun.csv", sep="")
FONT_SIZE = 14
WIDTH = 15 
HEIGHT = 10

# We combine in two files all the metrics (by run in a file, and aggregating by the median in a different file)
combineAndAggregateData (inputFileForMetrics =DATA_FILE_FOR_METRICS,
                         inputFileForApkSizes=DATA_FILE_FOR_APKSIZES,
                         inputFileForPermissions=DATA_FILE_FOR_PERMISSIONS,
                         outputFileForMetrics=OUTPUT_FILE_FOR_METRICS, 
                         outputFileForApkSizes=OUTPUT_FILE_FOR_APKSIZES,
                         outputFileForPermissions=OUTPUT_FILE_FOR_PERMISSIONS,
                         outputFileAllData=OUTPUT_FILE_ALL_DATA,
                         outputFileAllDataByRun=OUTPUT_FILE_ALL_DATA_BY_RUN)

# Read data
allData = fread(OUTPUT_FILE_ALL_DATA, header = T, sep = ',', stringsAsFactors = T)
allData = subset(allData, individual != "nosdk")
allData[variable=="Network"]$value = allData[variable=="Network"]$value/1024
allDataByRun = fread(OUTPUT_FILE_ALL_DATA_BY_RUN, header = T, sep = ',', stringsAsFactors = T)
allDataByRun = subset(allDataByRun, individual != "nosdk")
allDataByRun[variable=="Network"]$value = allDataByRun[variable=="Network"]$value/1024

# Compute statistical differences using the Wilcoxon test
computeStatisticalTests(inputData = subset(allDataByRun,individual != "nosdk"),
                        pvalueToUse = 0.05,
                        outputFile = paste(OUTPUT_FOLDER, "statisticalTests.csv",sep=""))
statisticalTests = read.csv(paste(OUTPUT_FOLDER, "statisticalTests.csv",sep=""), stringsAsFactors = T)
statisticalTests = statisticalTests[order(statisticalTests$firstIndividual, statisticalTests$secondIndividual, statisticalTests$group, statisticalTests$variable),]

# Compute differences in %
computeDifferences(inputData = allData,
                   outputFile = paste(OUTPUT_FOLDER, "differences.csv",sep=""));
differences = read.csv(paste(OUTPUT_FOLDER, "differences.csv",sep=""), stringsAsFactors = T)
differences = differences[order(differences$firstIndividual, differences$secondIndividual, differences$group, differences$variable),]
differences$pvalue = statisticalTests$pvalue
differences$significant = statisticalTests$significant
differences$effect = statisticalTests$effect
write.csv(x = differences, paste(OUTPUT_FOLDER,"differencesWithStatisticalTests.csv",sep=""),row.names = F)
differences = subset(differences, variable %in% c("APK size", "Permissions", "Energy","CPU","Memory","Network"))
differences$variable <- factor(differences$variable, c("APK size", "Permissions", "Energy","CPU","Memory","Network"))

# Generate plot about differences
generatePlotForDifferencesByGroup (inputData = differences,
                                   onlySignificantData=T,
                                   outputFolder = OUTPUT_FOLDER,
                                   heightToUse = HEIGHT/2.5,
                                   widthToUse = WIDTH,
                                   fontSize = FONT_SIZE)

# Generate boxplots
variablesToUse = c("APK size", "Permissions", "Energy", "CPU", "Memory", "Network")
allDataByRun$variable <- factor(allDataByRun$variable, variablesToUse)
generateBoxplotsByGroup (inputData = allDataByRun,
                  groupsToUse = unique(allDataByRun$group),
                  variablesToUse = variablesToUse,
                  outputFolder = OUTPUT_FOLDER,
                  heightToUse = HEIGHT/2,
                  widthToUse = WIDTH,
                  fontSize = FONT_SIZE)
