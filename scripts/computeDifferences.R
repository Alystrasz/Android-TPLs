# This function computes the difference (raw value and %) for each variable and for all pair of elements in a given dataset.
# It is useful to generate different plots showing the existing difference between different TPLs and metrics.

computeDifferences <- function (inputData, 
                                outputFile = "")
{
  output = data.frame(stringsAsFactors = FALSE)
  
  groups = unique(inputData$group)
  for (groupToUse in groups)
  {
    individuals = unique(subset(inputData, group == groupToUse)$individual)
    for (indexFirstIndividual in 1:length(individuals))
    {
      indexSecondIndividual = indexFirstIndividual+1
      while (indexSecondIndividual <= length(individuals))
      {
        currentIndividuals = c(as.character(individuals[indexFirstIndividual]),as.character(individuals[indexSecondIndividual]))
        data = inputData[inputData$individual %in% currentIndividuals & inputData$group == groupToUse,]
        variables = unique(data$variable)
        
        for (variableToUse in variables)
        {
            dataUsed = subset(data, variable == variableToUse)
            firstIndividual = subset(dataUsed,individual == currentIndividuals[1])
            secondIndividual = subset(dataUsed,individual == currentIndividuals[2])
            
            difference = firstIndividual$value - secondIndividual$value
            if (firstIndividual$value > secondIndividual$value){
              percentage = (firstIndividual$value - secondIndividual$value)*100/firstIndividual$value
            } else {
              percentage = -((secondIndividual$value - firstIndividual$value)*100/secondIndividual$value)
            }
            
            row = cbind(currentIndividuals[1],currentIndividuals[2],groupToUse,variableToUse,as.double(firstIndividual$value), as.double(secondIndividual$value), as.double(difference),as.double(percentage))
            output = rbind(output,row)
        }
        indexSecondIndividual = indexSecondIndividual+1
        }
      }
  }
  
  colnames(output) = c("firstIndividual",
                       "secondIndividual",
                       "group",
                       "variable",
                       "firstValue",
                       "secondValue",
                       "difference",
                       "percentage")
  
  #It writes data to disk if it is required
  if (outputFile != "") {
    write.csv(x = output, file = outputFile, row.names = FALSE)
  } else {
    print(output)
  }
}
