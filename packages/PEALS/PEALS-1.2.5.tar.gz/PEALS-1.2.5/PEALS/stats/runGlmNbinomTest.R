#!/usr/bin/env Rscript

suppressMessages(library('getopt'))

command =  matrix(c(
    "help",         "h",   0,  "logical",     "Show help information (https://rstudio-pubs-static.s3.amazonaws.com/329027_593046fb6d7a427da6b2c538caf601e1.html)",
    "adjp",         "q",   2,  "numeric",     "adjp cutoff (0.1)",
    "cpu",          "c",   1,  "numeric",     "Threads used for DESeq()",
    "counts",       "g",   1,  "character",   "peakid-counts matrix (peakid in 1st column)",
    "fittype",      "y",   1,  "character",   "the fitType in DESeq() (parametric[default]local|mean|glmGamPoi)",
    "formula",      "k",   1,  "character",   "The design formula in DESeqDataSetFromMatrix() function (eg. antibody + genotype + genotype:antibody)",
    "mean",         "f",   2,  "integer",     "baseMean for ploting barplot",
    "name",         "n",   1,  "character",   "Name for extract the results formula in results() (eg. antibodyip.genotypetreat for treat (ip vs input) vs ko (ip vs input) )",
    "output" ,      "o",   1,  "character",   "Output directory",
    "plot",         "p",   0,  "logical",     "Set to plot the output",
    "padjust",      "j",   1,  "character",   "The method to use for adjusting p-values, see ?p.adjust",
    "temp",         "T",   1,  "character",   "Prefix for temporary output (including path)",
    "prefix",       "e",   1,  "character",   "Prefix for output",
    "reduced",      "i",   1,  "character",   "The reduced formula for DESeq(dds, test=\"LRT\", reduced=)",
    "relevel",      "w",   1,  "character",   "Relevel the sample data for comparison (eg. 'genotype:control,antibody:input', 'control' and 'input' will set as ref)",
    "sample",       "m",   1,  "character",   "Sample relationships matrix",
    "sep",          "r",   1,  "character",   "The separator for peakid",
    "shrink",       "s",   1,  "character",   "Shrinkage method for DE results (none|normal|apeglm[default]|ashr)",
    "skipsize",     "S",   0,  "logical",     "Skip to calculate the sizeFactor",
    "skipsubplot",  "P",   0,  "logical",     "Set to plot plots for non-peak",
    "test",         "t",   1,  "character",   "The test method for p-value (Wald|LRT)"
), byrow=TRUE, ncol=5)

# function
ShowHelp <- function(object, param, reverse=FALSE, bool=FALSE) {
  if (reverse) {
    if (bool) {
      judge <- !isTRUE(object)
    }else{
      judge <- !is.null(object)
    }
  }else{
    if (bool) {
      judge <- isTRUE(object)
    }else{
      judge <- is.null(object)
    }
  }
  if (judge) {
    if (param != 'none') {
      cat(paste("None valid ", param, "!\n"))
    }
    cat(paste(getopt(command, usage = T),"\n"))
    q()
  }
}

LoadPacakge <- function(name) {
  suppressMessages(library(name, character.only = TRUE))
  message(paste("Load package: ", name, ", version: ", packageVersion(name), "."))
}

## output function
DfwriteToFile <- function(df, prefix, appendix) {
  ## the prefix including path
  resultFile <- paste(prefix, appendix, sep="")
  output.file <- file(resultFile, "wb")
  df <- cbind(peakid = rownames(df), df)
  write.table(as.data.frame(df), sep="\t", eol = "\n", 
              quote = FALSE, row.names=FALSE, file=output.file)
  close(output.file)
}

# supress warnings
options(warn=-1)
# parsing arguments
args <- getopt(command)

ShowHelp(args$help, 'none', TRUE)
ShowHelp(args$counts, '-g|--counts')
ShowHelp(args$sample, '-s|--sample')

if (is.null(args$name)) {
  ShowHelp(args$name, '-n|--name')
}

if (is.null(args$formula)) {
  ShowHelp(args$formula, '-k|--formula')
}

if ( is.null(args$test) ) {
  args$test = 'Wald'
}else{
  testVetor <- c('Wald', 'LRT')
  bool <- isFALSE(args$test %in% testVetor)
  ShowHelp(bool, '-T|--test', FALSE, TRUE)
}

if ( is.null(args$shrink) ) {
  args$shrink = 'apeglm'
}else{
  shrinkVetor <- c('none', 'normal', 'apeglm', 'ashr')
  bool <- isFALSE(args$shrink %in% shrinkVetor)
  ShowHelp(bool, '-s|--shrink', FALSE, TRUE)
}

if ( is.null(args$fittype) ) {
  args$fittype = 'parametric'
}else{
  fitTypeVetor <- c("parametric", "local", "mean", "glmGamPoi")
  bool <- isFALSE(args$fittype %in% fitTypeVetor)
  ShowHelp(bool, '-y|--fitType', FALSE, TRUE)
}

# default values
if ( is.null(args$mean) ) { args$mean = 1 }
if ( is.null(args$adjp) ) { args$adjp = 0.1 }
if ( is.null(args$padjust) ) { args$padjust = "BH" }
if ( is.null(args$prefix) ) { args$prefix = 'result' }
if ( is.null(args$output) ) { args$output = './' }
if ( is.null(args$sep) ) { args$sep = '|=' }
# load DESeq2 and perform Differential Analysis
LoadPacakge('DESeq2')
LoadPacakge('ggplot2')
#LoadPacakge("BiocParallel")
#register(MulticoreParam(args$cpu))

if ( is.null(args$cpu) ) {
  args$cpu = 1
}

## load arguments
mean <- args$mean
tempPrefix <- args$temp
fitType <- args$fittype
test <- args$test
shrink <- args$shrink
prefix <- args$prefix
output <- args$output

########################################## main ###########################################
# With the count matrix, cts, and the sample information, colData
cts <- as.matrix(read.csv(args$counts, sep="\t", row.names=1))
cts <- round(cts, 0)
colData <- read.csv(args$sample, row.names=1, sep="\t")

## convert into factor
colData[] <- lapply( colData, factor)

if (test == "LRT") {
  if (is.null(args$reduced)) {
    bool <- TRUE
    ShowHelp(bool, '-i|--reduced', FALSE, TRUE)
  }
}

# check all sample rownames in geneCountMtx colNames
all(rownames(colData) %in% colnames(cts))
cts <- cts[, rownames(colData)]

designFormula <- as.formula(paste("~", args$formula, sep=""))
print(designFormula)

# construct a DESeqDataSet object
dds <- DESeqDataSetFromMatrix(countData = cts, colData = colData, design = designFormula)

## relevel the dds
## "genotype:control,antibody:input"
relevelVector <- unlist(strsplit(args$relevel, ","))
##[1] "genotype:control" "antibody:input"
for (eachRelevel in relevelVector) {
  eachRelevelVector <- unlist(strsplit(eachRelevel, ":"))
  relevelName <- eachRelevelVector[1]
  relevelVal <- eachRelevelVector[2]
  dds[[relevelName]] <- relevel(dds[[relevelName]], relevelVal)
}

featureData <- data.frame(gene=rownames(cts))
mcols(dds) <- DataFrame(mcols(dds), featureData)

if (! is.null(args$reduced) && test != "Wald") {
  reduced <- as.formula(paste("~", args$reduced, sep=""))
}

print(args$test)
print(args$fittype)

# runing DESeq
dds <- estimateSizeFactors(dds)
## setting the size factor as 1
if (! is.null(args$skipsize)) {
  sizeFactors(dds) = 1
}

dds <- estimateDispersions(dds, fitType=args$fittype)

if (test == "LRT") {
  dds <- nbinomLRT(dds, reduced = reduced)
}else{
  dds <- nbinomWaldTest(dds)
}

## output sizeFactor
sizeFactorDf <- as.data.frame(as.matrix(dds$sizeFactor))
# structure
##               V1
## ip_1_1      0.8683194
## ip_1_0      0.8721959
## input_0_1   1.2220192
## input_0_0   1.1333223

DfwriteToFile(sizeFactorDf, tempPrefix, '.sizefactor.txt')

## continue
resultsNameVector <- resultsNames(dds)

print(resultsNameVector)
print(args$name)

if ( shrink != 'none' ) {
  res <- lfcShrink(dds, coef=args$name, type=args$shrink, apeMethod="nbinomC")
}else{
  res <- results(dds, pAdjustMethod=args$padjust, name=args$name)
}

# to avoid NA adjusted p-values
res$padj <- p.adjust(res$pvalue, method="BH")

########################################## result files ###########################################
# output DESeq2 result
DfwriteToFile(as.data.frame(res), tempPrefix, ".glm.txt")

# output normalzed counts
normalzedCounts <- counts(dds, normalized=TRUE)
DfwriteToFile(as.data.frame(normalzedCounts), tempPrefix, ".normalized.counts.txt")

########################################## plots ###########################################
## plot functions
getPdfFile <- function(output, prefix, appendix) {
  pdfFile <- file.path(output, paste(prefix, appendix, sep=""))
  return(pdfFile)
}

plotDisper <- function(dds, pdf) {
  pdf(pdf, paper='a4r', height=0)
  plotDispEsts(dds)
  garbage <- dev.off()
}

plotMa <- function(res, alpha, pdf) {
  pdf(pdf, paper='a4r', height=0)
  DESeq2::plotMA(res, ylim=c(-6,6), alpha=alpha, cex=0.6)
  abline(h=c(-1,1), col="dodgerblue", lwd=2)
  garbage <- dev.off()
}

plotHist <- function(res, mean, pdf) {
  pdf(pdf, paper='a4r', height=0)
  hist(res$pvalue[res$baseMean > mean], breaks = 0:20/20,
       col = "grey50", border = "white", 
       xlab = 'p-value', main = paste('Histogram of p-value (baseMean > ', mean, ')', sep=""))
  garbage <- dev.off()
}

ploBar <- function(resLFC1, pdf) {
  qs <- c(0, quantile(resLFC1$baseMean[resLFC1$baseMean > 0], 0:6/6))
  bins <- cut(resLFC1$baseMean, qs)
  levels(bins) <- paste0("~", round(signif((qs[-1] + qs[-length(qs)])/2, 2)))
  fractionSig <- tapply(resLFC1$pvalue, bins, function(p)
                            mean(p < 0.05, na.rm = TRUE))
  pdf(pdf, paper='a4r', height=0)
  barplot(fractionSig, xlab = "Mean normalized count",
                       ylab = "Fraction of small p values")
  garbage <- dev.off()
}

sepRegex = gsub("\\|", "\\\\|", args$sep)
peakRegex = paste(sepRegex, '\\d+', sepRegex, 'T$', sep='')
nonpeakRegex = paste(sepRegex, '\\d+', sepRegex, 'F$', sep='')

if ( ! is.null(args$plot) ) {
  ## dispersion
  # output dispersion for peaks and non-peaks
  outputPdf <- getPdfFile(output, prefix, ".dispersion.all.pdf")
  pdf(outputPdf, paper='a4r', height=0)
  plotDispEsts(dds)
  garbage <- dev.off()
  #plotDisper(dds, outputPdf)
  if (is.null(args$skipsubplot)){
    # plot dispersion plot for peaks only
    subDds <- dds[ grep(peakRegex, rownames(dds)), ]
    outputPdf <- getPdfFile(output, prefix, ".dispersion.peak.pdf")
    pdf(outputPdf, paper='a4r', height=0)
    plotDispEsts(subDds)
    garbage <- dev.off()
    #plotDisper(subDds, outputPdf)
    # plot dispersion plot for npon-peaks only
    subDds <- dds[ grep(nonpeakRegex, rownames(dds)), ]
    outputPdf <- getPdfFile(output, prefix, ".dispersion.nonpeak.pdf")
    pdf(outputPdf, paper='a4r', height=0)
    plotDispEsts(subDds)
    garbage <- dev.off()
    #plotDisper(subDds, outputPdf)
  }
  
  ## MA
  # plot MA plot for peaks and non-peaks
  outputPdf <- getPdfFile(output, prefix, ".MA.all.pdf")
  pdf(outputPdf, paper='a4r', height=0)
  DESeq2::plotMA(res, ylim=c(-6,6), alpha=args$adjp, cex=0.6)
  abline(h=c(-1,1), col="dodgerblue", lwd=2)
  garbage <- dev.off()
  #plotMa(res, args$adjp, outputPdf)
  if (is.null(args$skipsubplot)){
    # plot MA plot for peaks only
    subRes <- res[ grep(peakRegex, row.names(res)), ]
    outputPdf <- getPdfFile(output, prefix, ".MA.peak.pdf")
    pdf(outputPdf, paper='a4r', height=0)
    DESeq2::plotMA(subRes, ylim=c(-6,6), alpha=args$adjp, cex=0.6)
    abline(h=c(-1,1), col="dodgerblue", lwd=2)
    garbage <- dev.off()
    #plotMa(subRes, args$adjp, outputPdf)
    # plot MA plot for non-peaks only
    subRes <- res[ grep(nonpeakRegex, row.names(res)), ]
    outputPdf <- getPdfFile(output, prefix, ".MA.nonpeak.pdf")
    pdf(outputPdf, paper='a4r', height=0)
    DESeq2::plotMA(subRes, ylim=c(-6,6), alpha=args$adjp, cex=0.6)
    abline(h=c(-1,1), col="dodgerblue", lwd=2)
    garbage <- dev.off()
  }
  #plotMa(subRes, args$adjp, outputPdf)
  
  ## histogram
  # plot the histogram of the p values for peaks and non-peaks
  outputPdf <- getPdfFile(output, prefix, ".pvalue.histogram.all.pdf")
  pdf(outputPdf, paper='a4r', height=0)
  hist(res$pvalue[res$baseMean > mean], breaks = 0:20/20,
       col = "grey50", border = "white", 
       xlab = 'p-value', main = paste('Histogram of p-value (baseMean > ', mean, ')', sep=""))
  garbage <- dev.off()
  #plotHist(res, args$mean, outputPdf)
  
  # plot the histogram of the p values for non-peaks only
  if (is.null(args$skipsubplot)){
    # plot the histogram of the p values for peaks only
    subRes <- res[ grep(peakRegex, row.names(res)), ]
    outputPdf <- getPdfFile(output, prefix, ".pvalue.histogram.peak.pdf")
    pdf(outputPdf, paper='a4r', height=0)
    hist(subRes$pvalue[subRes$baseMean > mean], breaks = 0:20/20,
         col = "grey50", border = "white", 
         xlab = 'p-value', main = paste('Histogram of p-value (baseMean > ', mean, ')', sep=""))
    garbage <- dev.off()
    #plotHist(subRes, args$mean, outputPdf)
    subRes <- res[ grep(nonpeakRegex, row.names(res)), ]
    outputPdf <- getPdfFile(output, prefix, ".pvalue.histogram.nonpeak.pdf")
    pdf(outputPdf, paper='a4r', height=0)
    hist(subRes$pvalue[subRes$baseMean > mean], breaks = 0:20/20,
         col = "grey50", border = "white", 
         xlab = 'p-value', main = paste('Histogram of p-value (baseMean > ', mean, ')', sep=""))
    garbage <- dev.off()
  }
  #plotHist(subRes, args$mean, outputPdf)
  
  if (test == "Wald") {
    ## bar
    resLFC1 <- results(dds, pAdjustMethod=args$padjust, lfcThreshold=1)
    # The ratio of small p values for genes binned by mean normalized count for peaks and non-peaks
    outputPdf <- getPdfFile(output, prefix, ".pvalueNorCounts.bar.all.pdf")
    qs <- c(0, quantile(resLFC1$baseMean[resLFC1$baseMean > 0], 0:6/6))
    bins <- cut(resLFC1$baseMean, qs)
    levels(bins) <- paste0("~", round(signif((qs[-1] + qs[-length(qs)])/2, 2)))
    fractionSig <- tapply(resLFC1$pvalue, bins, function(p)
                              mean(p < 0.05, na.rm = TRUE))
    pdf(outputPdf, paper='a4r', height=0)
    barplot(fractionSig, xlab = "Mean normalized count",
                         ylab = "Fraction of small p values")
    garbage <- dev.off()
    #ploBar(resLFC1, outputPdf)
    # The ratio of small p values for genes binned by mean normalized count on non-peaks only
    if (is.null(args$skipsubplot)){
      # The ratio of small p values for genes binned by mean normalized count on peaks only
      subResLFC1 <- resLFC1[ grep(peakRegex, row.names(resLFC1)), ]
      outputPdf <- getPdfFile(output, prefix, ".pvalueNorCounts.bar.peak.pdf")
      qs <- c(0, quantile(subResLFC1$baseMean[subResLFC1$baseMean > 0], 0:6/6))
      bins <- cut(subResLFC1$baseMean, qs)
      levels(bins) <- paste0("~", round(signif((qs[-1] + qs[-length(qs)])/2, 2)))
      fractionSig <- tapply(subResLFC1$pvalue, bins, function(p)
                                mean(p < 0.05, na.rm = TRUE))
      pdf(outputPdf, paper='a4r', height=0)
      barplot(fractionSig, xlab = "Mean normalized count",
                           ylab = "Fraction of small p values")
      garbage <- dev.off()
      #ploBar(subResLFC1, outputPdf)
      subResLFC1 <- resLFC1[ grep(nonpeakRegex, row.names(resLFC1)), ]
      outputPdf <- getPdfFile(output, prefix, ".pvalueNorCounts.bar.nonpeak.pdf")
      qs <- c(0, quantile(subResLFC1$baseMean[subResLFC1$baseMean > 0], 0:6/6))
      bins <- cut(subResLFC1$baseMean, qs)
      levels(bins) <- paste0("~", round(signif((qs[-1] + qs[-length(qs)])/2, 2)))
      fractionSig <- tapply(subResLFC1$pvalue, bins, function(p)
                                mean(p < 0.05, na.rm = TRUE))
      pdf(outputPdf, paper='a4r', height=0)
      barplot(fractionSig, xlab = "Mean normalized count",
                           ylab = "Fraction of small p values")
      garbage <- dev.off()
    }
    #ploBar(subResLFC1, outputPdf)
  }
}
