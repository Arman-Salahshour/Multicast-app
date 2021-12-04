host='127.0.0.1'
port=65432
txt_messageSize=1024
img_messageSize=4096
multicast_groupIP='224.0.0.0'
multicast_groupPort=10000
format='utf-8'

'''constant messages'''
rqst_forTimeSchedule="send programs' time schedule"
rqst_forImg="send current movie"
rqst_forIpPort="send channels' ip and port"
msg_active="msg: this chanel is active"
end_moviesMsg="end of movies' schedule message"
end_liveMovieNameMsg="end of live movie name message"
end_liveMovieSizeMsg="end of live movie size message"
end_liveMovieImgsMsg="end of live movie imgs message"
end_sending="The end"
