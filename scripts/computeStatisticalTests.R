# This function computes statistical test to check whether differences are significant between each pair of individuals (TPLs) and for each variable (metric).
# It applies the Wilcoxon test and, if the obtained p-value is lower than the given threshold, the effect size is computed using the cliff.delta function.

library(effsize)

computeStatisticalTests <- function (inputData,
                                     pvalueToUse = 0.05,
                                     outputFile = "")
{
  output = data.frame()

  groupsToUse = unique(inputData$group)
  for (groupToUse in groupsToUse)
  {
    dataInCurrentGroup = subset(inputData, group == groupToUse)
    individualsToUse = unique(dataInCurrentGroup$individual)
    
    for (indexFirstIndividual in 1:length(individualsToUse))
    {
      indexSecondIndividual = indexFirstIndividual+1
      while (indexSecondIndividual <= length(individualsToUse))
      {
        currentIndividuals = c(as.character(individualsToUse[indexFirstIndividual]),as.character(individualsToUse[indexSecondIndividual]))
        
        # Format data
        data = dataInCurrentGroup[dataInCurrentGroup$individual %in% currentIndividuals,]
        
        variablesToUse = unique(data$variable)
        for (variableToUse in variablesToUse)
        {
          dataUsed = subset(data, variable == variableToUse)
          
          dataForFirstIndividual = dataUsed[dataUsed$individual == currentIndividuals[1],]
          dataForSecondIndividual = dataUsed[dataUsed$individual == currentIndividuals[2],]
          
          if (nrow(dataForFirstIndividual) == 1 & nrow(dataForSecondIndividual) == 1)
          {
            significant = 1
            pvalue = 0
            effect = NA
          }
          else {
            result = wilcox.test(dataForFirstIndividual$value, dataForSecondIndividual$value)
            pvalue = result$p.value
            if (is.nan(pvalue)) {
              significant = NA
              effect = "-"
            } else if (pvalue <= pvalueToUse){
              significant = 1
              effect = as.character(cliff.delta(dataForFirstIndividual$value, dataForSecondIndividual$value)$magnitude)
            }else{
              significant = 0
              effect = "-"
            } 
          }
          
          row = cbind(currentIndividuals[1],currentIndividuals[2],as.character(groupToUse),as.character(variableToUse),pvalue,significant,effect)
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
                       "pvalue",
                       "significant",
                       "effect")
  #It writes data to disk if it is required
  if (outputFile != "") {
    write.csv(x = output, file = outputFile, row.names = FALSE)
  } else {
    print(output)
  }
}
