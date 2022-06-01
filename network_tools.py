import pickle


def encode_flag_data(flag, data=' '):
    if not isinstance(flag, str) or len(flag) != 2:
        raise ValueError('Invalid flag!')

    return flag.encode() + pickle.dumps(data)


def decode_flag_data(msg):
    if len(msg) > 2:
        flag = msg[:2]
        flag = flag.decode()
        pickled_data = msg[2:]
        data = pickle.loads(pickled_data)

        return flag, data
    else:
        return msg.decode(), None
