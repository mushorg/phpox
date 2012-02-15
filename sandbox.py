import sys

import sink.hpf_sink as hpf_sink


def main():
    hpf_sink.run()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
