badges_markdown = function(repo)
{
  link = function(w, l) {
    if (!RCurl::url.exists(l))
      return(w)
    
    paste0("[", w, "](", l, ")")
    
  }
  
  wflow = c("R-CMD-check", "pkgdown")
  
  # Badge template
  tmp_cmd1 = "https://github.com/caravagnalab/PKG/workflows/WKF/badge.svg"
  tmp_cmd2 = "https://github.com/caravagnalab/PKG/actions/workflows/WKF.yaml"
  
  tmp_cmd1 = gsub("PKG", repo, tmp_cmd1)
  tmp_cmd2 = gsub("PKG", repo, tmp_cmd2)
  
  # Homepage
  www = "https://caravagnalab.github.io/PKG/"
  www = link(repo, gsub("PKG", repo, www))
  
  # Workflows
  wflows = c()
  
  for(w in wflow)
  {
    badge = paste0("!", link(w, gsub("WKF", w, tmp_cmd1)))
    badge_link = link(badge, gsub("WKF", w, tmp_cmd2))  
    
    wflows = c(wflows, badge_link)
  }

  pool = append(list(www), wflows)
  names(pool) = c("Tool", wflow)
  
  pool
}

# Packages
packages = c("BMix", 
             "CNAqc", 
             "congas",
             "ctree", 
             "mobster", 
             "mtree", 
             "Rcongas", 
             "revolver", 
             "TINC", 
             "VIBER")

packages = lapply(packages, badges_markdown)

# Header
columns = names(packages[[1]])
columns = paste(columns, collapse =  " | ")

# Newline
nl = rep('----', length(packages[[1]]))
nl = paste0(nl, collapse =  " | ")

# Badges/links 
badges = sapply(packages, function(x){
  paste0(
    x, collapse = " |"
  )
})

# Table
markdown_table = paste(
  c(
    columns,
    nl,
    badges),
  collapse = '\n'
)

cat(markdown_table)
