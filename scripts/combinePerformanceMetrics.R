# This script reads CSV files of energy consumption and CPU, memory, and network usages and combines all the information in a new CSV file.
# Energy consumption is measured in Joules (J).
# CPU usage is measured in %.
# Memory usage is measured in megabytes (MB).
# Network usage us measured in kilobytes (kB).

require(data.table)

# Constants
PATH = "/Experiments/"
OUTPUT_FOLDER = paste(PATH,"results/",sep="")
OUTPUT_FILE = paste(OUTPUT_FOLDER,"metrics.csv", sep="")
DATA_FILE_FOR_ENERGY = paste(PATH,"results/energyByRun.csv", sep="")
DATA_FILE_FOR_MEMORY_AND_CPU = paste(PATH,"results/memoryAndCPUByRun.csv", sep="")
DATA_FILE_FOR_NETWORK = paste(PATH,"results/networkByRun.csv", sep="")

# Read energy consumption from CSV files
energy = fread(DATA_FILE_FOR_ENERGY, header = T, sep = ',', stringsAsFactors = F)
allData=data.frame(energy$SdkName,energy$SdkType,"Energy",energy$Run,energy$Value, stringsAsFactors = F)
colnames(allData) = c("SdkName","SdkType","Metric","Run","Value")
rm(energy)

# Read memory and CPU usages from CSV files
memoryAndCPU = fread(DATA_FILE_FOR_MEMORY_AND_CPU, header = T, sep = ',', stringsAsFactors = F)
memoryAndCPU = subset(memoryAndCPU, select=c("SdkName","SdkType","Metric","Run","AvgValue"))
colnames(memoryAndCPU) = c("SdkName","SdkType","Metric","Run","Value")
memory = subset(memoryAndCPU, Metric == "Memory")
memory$Value = memory$Value/1024
cpu = subset(memoryAndCPU, Metric == "CPU")
allData=rbind(allData,memory,cpu)
rm(memoryAndCPU, memory, cpu)

# Read network usage from CSV files
network = fread(DATA_FILE_FOR_NETWORK, header = T, sep = ',', stringsAsFactors = F)
network=data.frame(network$SdkName,network$SdkType,"Network",network$Run,network$Bytes, stringsAsFactors = F)
colnames(network) = c("SdkName","SdkType","Metric","Run","Value")
network$Value = network$Value/1024
allData=rbind(allData,network)
rm(network)

#Write output dataframe
write.csv(allData, file = OUTPUT_FILE, row.names = FALSE)
