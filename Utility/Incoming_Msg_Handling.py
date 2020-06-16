# ****
# IMPORTS
# ****

import Utility_Server_Main as USM




# ****
# TAGS
# ****

SUFFIX_TAG = '[SUFFIX_CALCULATOR]'
HANG_MAN_TAG = '[HANG_MAN]'
CHAT_ROOM_TAG = '[CHAT_ROOM]'


def message_Handling(result):
    if SUFFIX_TAG in result:
        USM.Update_Suffix_Calculator(result)


    if HANG_MAN_TAG in result:
        USM.Update_Hang_Man(result)

    if CHAT_ROOM_TAG in result:
        USM.Update_Chat(result)

