# This function generates boxplots for all the groups and variables in the input dataset.
# It is useful to show the distribution of metric values for TPLs.

require(ggplot2)

generateBoxplotsByGroup <- function (inputData,
                              groupsToUse,
                              variablesToUse,
                              outputFolder = "",
                              heightToUse = 5,
                              widthToUse = 5,
                              fontSize = 14)
{
  dataToUse = subset(inputData, variable %in% variablesToUse)
  dataToUse$variable <- factor(dataToUse$variable, variablesToUse)
   
  for (groupToUse in groupsToUse) {
    #It creates pdf file if it is required
    if (outputFolder != "")
    {
      pdf(paste(outputFolder, "Boxplot-",groupToUse,".pdf",sep=""), height = heightToUse, width = widthToUse)
    }
    
    #It generates the boxplots
    p <- ggplot(data = subset(dataToUse, group == groupToUse), aes(x=individual, y=value)) 
    p <- p + geom_boxplot(aes(fill=individual))
    p <- p + scale_y_continuous(breaks = scales::pretty_breaks(n = 8))
    p <- p + facet_wrap( ~ variable, scales="free", ncol=length(variablesToUse))
    p <- p + stat_summary(fun.y = "mean", geom = "point", shape= 23, size= 4, fill= "white")
    p <- p + xlab("") + ylab("") + ggtitle("")
    p <- p + theme(legend.position='none', 
                   text = element_text(size = fontSize),
                   strip.text = element_text(size=fontSize),
                   axis.title.x = element_text(size = fontSize),
                   axis.title.y = element_text(size = fontSize),
                   axis.text.x = element_text(angle = 45, hjust = 1, size = fontSize),
                   axis.text.y = element_text(size = fontSize))
    
    #It saves the plot to a file or it shows it
    if (outputFolder != "")
    {
      print(p)
      dev.off()
    }
    else
    {
      p
    }
  }
}
