from speak_to_file.speak_to_file import *

logger = logging.getLogger(__name__)
logger.warning("Boop")

def fun_test(fun, args, output):
    if type(args) == list:
        try:
            fun_result = fun(*args)
            exception = None
        except Exception as e:
            fun_result = None
            exception = e
    elif type(args) == dict:
        try:
            fun_result = fun(**args)
            exception = None
        except Exception as e:
            fun_result = None
            exception = e
    else:
        try:
            fun_result = fun()
            exception = None
        except Exception as e:
            fun_result = None
            exception = e

    outcome = output == fun_result

    result = {
        "Function": fun.__name__, 
        "Result": "Error" if exception is not None else "Success" if outcome else "Failure",
        "Expected": output,
        "Got": fun_result,
        "Exception": exception
    }

    return(result)
    
scenarios = [
    {
        "fun": replace_invalid_chars,
        "input": ["""<>:"\|?*"""],
        "output": ""
    },
    {
        "fun": glue_args,
        "input": [{'-hide_banner': True, '-i': 'pipe:0',  '-c:a': 'libvorbis',  '-q:a': '1', '-ac': '1', '-ar': '22050', '-y': True}],
        "output": ['-hide_banner', '-i', 'pipe:0', '-c:a', 'libvorbis', '-q:a', '1', '-ac', '1', '-ar', '22050', '-y']
    },
    {
        "fun": split_args,
        "input": ["-hide_banner=,-i=pipe:0,-c:a=libvorbis,-q:a=1,-ac=1,-ar=22050,-y="],
        "output": {'-hide_banner': True, '-i': 'pipe:0',  '-c:a': 'libvorbis',  '-q:a': '1', '-ac': '1', '-ar': '22050', '-y': True}
    }
]


if __name__ == "__main__":
    result = []
    for scenario in scenarios:
        result.append(fun_test(fun = scenario["fun"], args = scenario["input"], output = scenario["output"]))

    print(*result, sep = "\n")
