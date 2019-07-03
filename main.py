#-*-coding:utf8;-*-
from Tvshows4mobile import Tvshows4mobile

tvseries = Tvshows4mobile()

def main():
    while 1:
        user_input = raw_input(">>>>> ")
        if tvseries.can_process(user_input):
            response = tvseries.run_download(user_input)
            print(response)
        else:
            print("unrecognised command")

if __name__ == "__main__":
    main()