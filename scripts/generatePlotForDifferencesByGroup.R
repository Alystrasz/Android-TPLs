# This function makes a pairwise comparison of individuals (TPLs) and variables (metrics) in a graphical way.
# It generates a matrix where each cell contains the difference of the medians in \%, the magnitude of the difference, and the magnitude of the effect size (small, medium, or large) for each metric and pair of TPLs. 
# The effect size is ``NA'' when it does not apply (for exmaple, for APK size and number of permissions metrics where we only have a measurement for each TPL).
# Absent values in the matrix indicate cases where there is not a statistically significant difference.

#!/usr/bin/env Rscript
require(ggplot2)
require(gridExtra)
require(gtable)
library(stringr)

generatePlotForDifferencesByGroup <- function (inputData,
                                               onlySignificantData=T,
                                               outputFolder = "",
                                               heightToUse = 5,
                                               widthToUse = 5,
                                               fontSize = 16)
{
  dataToUsed=inputData    
  if (onlySignificantData) {
    dataToUsed=subset(dataToUsed, significant == 1)
  }
  else
  {
    dataToUsed[dataToUsed$significant == 1,]$significant = "*"
    dataToUsed[dataToUsed$significant == 0,]$significant = ""
  }
  dataToUsed=dataToUsed[order(dataToUsed$group,dataToUsed$variable,dataToUsed$firstIndividual),]
  dataToUsed$percentageInterval = cut(dataToUsed$percentage, breaks = c(-100, -70, -20, -10, 0, 10, 20, 70, 100), include.lowest = TRUE)
  
  for (groupToUse in unique(dataToUsed$group))
  {
    p <- ggplot(subset(dataToUsed, group == groupToUse), aes(x = firstIndividual, y = secondIndividual))
    p <- p + geom_tile(aes(fill = percentageInterval))
    p <- p + scale_fill_brewer(type = "div",
                               palette = "RdYlGn",
                               direction = -1,
                               drop = FALSE, 
                               guide = guide_legend(reverse = FALSE,
                                                    nrow=1,
                                                    byrow=TRUE), 
                               name = paste("differences (in %): ",sep=""))
    p <- p + scale_y_discrete(drop = TRUE)
    if (onlySignificantData) {
      p <- p + geom_text(aes(label = paste(fmt(percentage), "%","\n(",fmt(firstValue - secondValue),")\n",effect,sep="")), 
                         size = 4.2, 
                         color="black")
    }
    else {
      p <- p + geom_text(aes(label = paste(fmt(percentage), "%", significant, "\n(",fmt(firstValue - secondValue),")\n",effect,sep="")), 
                         size = 4.2, 
                         color="black") 
    }
    p <- p + facet_grid(~variable, scales = "fixed", space = "fixed", drop=F)
    p <- p + labs(x = "", y = "")
    p <- p + theme_complete_bw(base_size = fontSize, legend_position = "top")
    
    if (outputFolder != "")
    {
      cairo_pdf(file = paste(outputFolder,"Differences-", groupToUse,".pdf",sep=""),width = widthToUse, height = heightToUse)
      print(p)
      dev.off()
    }
    else
    {
      print(p)
    }
  }
}

theme_complete_bw = function(base_size = 11, base_family = "", legend_position="none") {
  theme_bw(base_size = base_size, base_family = base_family) %+replace%
    theme(
      axis.text.x        = element_text(angle = 0, size = base_size),
      axis.text.y        = element_text(angle = 90, size = base_size),
      axis.title         = element_text(face = "bold", size = base_size),
      legend.position    = legend_position,
      legend.justification=c(1, 1),
      legend.direction   ="horizontal",
      #legend.key         = element_rect(fill = "grey95", colour = "black"),
      legend.key.size    = unit(1, "lines"),
      legend.title       = element_text(size = base_size),
      legend.text        = element_text(size = base_size),
      panel.border       = element_rect(fill = NA, colour = "black"),
      panel.grid.major   = element_blank(),
      panel.grid.minor   = element_blank(),
      plot.title         = element_blank(),
      strip.background   = element_rect(fill = NA, colour = NA),
      strip.text         = element_text(size = base_size)
    )
}

fmt = function(x) { gsub(" ", "", format(round(x,2), nsmall = 2)) }
