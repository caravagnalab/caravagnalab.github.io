require(dplyr)

markdown_link =   link = function(pointer, url) {
  if (!RCurl::url.exists(url))
    return(pointer)
  
  paste0("[", pointer, "](", url, ")")
}

package_logo_html = function(repo){
  img_url = paste0(
    "https://caravagnalab.github.io/", repo, "/reference/figures/logo.png"
  )
  
  if (!RCurl::url.exists(img_url))
    return(repo)
  
  paste0("<img src=\"", img_url, "\" width=49px></img>")
}

package_homepage = function(repo){
   paste0("https://caravagnalab.github.io/", repo)
}

action_status = function(repo, workflow)
{
  # Templates
  badge = paste0(
    "https://github.com/caravagnalab/", repo, "/workflows/", workflow, "/badge.svg"
    )
  
  action = paste0(
    "https://github.com/caravagnalab/", repo, "/actions/workflows/", workflow, ".yaml"
  )

  badge = paste0("!", markdown_link(repo, badge))
  action = markdown_link(badge, action)  
  
  action
}

package_status = function(repo)
{
  # link_title = paste(markdown_link(repo, package_homepage(repo)))
                     
  # cat(paste("\n#", link_title, "\n"))
  
  paste(
    # package_logo_html(repo),
    # link_title,
    package_logo_html(repo) %>% markdown_link(package_homepage(repo)),
    action_status(repo, "pkgdown"),
    action_status(repo, "R-CMD-check"),  
    sep = " | "
    ) 
}

# Packages
R_packages = c("BMix", 
             "CNAqc", 
             "ctree", 
             "mobster", 
             "mtree", 
             "Rcongas", 
             "revolver", 
             "TINC", 
             "VIBER",
             "basilica",
             "lineaGT", 
             "easypar",
             "pio")

Python_packages = c(
               "congas",
               "pyBasilica",
               "pyLineaGT")

output = "
---
output: github_document
---

Landing page for the *Cancer Data Science Laboratory (CDS)* at the
University of Trieste, Italy.

[![](https://img.shields.io/badge/CDS%20Lab%20Github-caravagnalab-seagreen.svg)](https://github.com/caravagnalab)
[![](https://img.shields.io/badge/CDS%20Lab%20webpage-https://www.caravagnalab.org/-red.svg)](https://www.caravagnalab.org/)


# R packages

| Tool | pkgdown | R CMD check |
|------|---------|-------------|
R_PKG


# Python packages

| Tool | pkgdown | R CMD check |
|------|---------|-------------|
P_PKG
"

R_str = sapply(R_packages, package_status)
R_str = paste(R_str, collapse = '\n') 

P_str = sapply(Python_packages, package_status)
P_str = paste(P_str, collapse = '\n') 

output = gsub("R_PKG", R_str, output) 
output = gsub("P_PKG", P_str, output) 

cat("------------------------------------\n")
cat(output)
cat("------------------------------------\n")

fileConn<-file("README.Rmd")
writeLines(output, fileConn)
close(fileConn)

knitr::knit('README.Rmd')

# # Header
# columns = names(packages[[1]])
# columns = paste(columns, collapse =  " | ")
# 
# # Newline
# nl = rep('----', length(packages[[1]]))
# nl = paste0(nl, collapse =  " | ")
# 
# # Badges/links 
# badges = sapply(packages, function(x){
#   paste0(
#     x, collapse = " |"
#   )
# })
# 
# # Table
# markdown_table = paste(
#   c(
#     columns,
#     nl,
#     badges),
#   collapse = '\n'
# )
# 
# cat(markdown_table)
