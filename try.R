#! /usr/bin/Rscript
library(syuzhet)
library(zoo)
#args = commandArgs()
path = "ed_analyse_pieces"
sub_dirs = list.dirs(path = path)

for (dir in sub_dirs[2:79]){
  csv_files = list.files(path = dir)
  new_csv = read.csv(paste(dir,"joy.csv",sep="/")) # create a new csv which contains all emotion coeffs
  new_csv$avgLexVal <- NULL
  for (i in csv_files)
  {
    if ( grepl(".csv",i) && !grepl("all_emo", i))
    {
      file_path = paste(dir,i,sep="/") # get paths to all csv files under a theater piece
      df = read.csv(file_path)$avgLexVal
      num_rows = length(df)
      pass_size = 10 # window size
      if(num_rows < 100){
        x_len = num_rows
        if(num_rows < 10){ # smaller than window size
          pass_size = num_rows
        }
      }else{
        x_len = 100
      }
      
      dct_values <- get_dct_transform(
        df, 
        low_pass_size = pass_size, 
        x_reverse_len = x_len,
        scale_vals = F,
        scale_range = T
      )
      repeated_times = ceiling(num_rows/100)
      final_dct_values = rep(dct_values, each = repeated_times)
      emotion_col_name = substring(i,1,nchar(i)-4)
      new_csv[emotion_col_name] = final_dct_values[1:num_rows]
      'plot(
        dct_values, 
        type ="l", 
        main = emotion_col_name, 
        xlab = "Narrative Time", 
        ylab = "Emotional Valence", 
        col = "red"
      )'
    }
  }
  new_csv$trust[1:10]
  write.csv(new_csv, paste(dir,"all_emo.csv",sep="/"), row.names=FALSE)

}







# print(df)

## rolling operations for univariate series
# rollmean(df, 10)

'plot(
  dct_values, 
  type ="l", 
  main ="sadness", 
  xlab = "Narrative Time", 
  ylab = "Emotional Valence", 
  col = "red"
)'

