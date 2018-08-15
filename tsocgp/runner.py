import argparse
import json

def main():
    parser = argparse.ArgumentParser(description='Attempts to schedule trains')
    parser.add_argument('file', metavar='N', type=argparse.FileType('r'), help="The json file to try and schedule trains for")

    args = parser.parse_args()
    #print(args.file)
    data = json.load(args.file)
    print(data.keys())
    #['label', 'hash', 'service_intentions', 'routes', 'resources', 'parameters']
    print(data['parameters'])
    print(data['label']) # Needed for problem_instance_label
    print(data['hash'])  # Needed for problem_instance_hash
    print("-----------------------------")
    print(data['service_intentions'])
    print("-----------------------------")
    print(data['routes'])
    print("-----------------------------")
    print(len(data['routes']))
    print(data['routes'][0])


if __name__ == "__main__":
    main()