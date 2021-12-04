'''general variables/ host and port are server's config'''
host='127.0.0.1'
port=65432
txt_messageSize=1024
img_messageSize=4096
format='utf-8'

'''constant messages'''
rqst_forTimeSchedule="channel:send programs' time schedule"
rqst_forImg="channel:send current movie"
client_rqstForImgs="client:send movie's frames"
msg_active="msg: this chanel is active"
msg_receiving="The end"
msg_receivingTimeSchedule="msg: receive programs' time schedule"
msg_receivingImgs="msg: receive program's images"
# end_moviesMsg="end of movies' schedule message"
# end_liveMovieNameMsg="end of live movie name message"
# end_liveMovieSizeMsg="end of live movie size message"
# end_liveMovieImgsMsg="end of live movie imgs message"