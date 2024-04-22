followers = []
following = []

res = set(following) - set(followers)
print(f'following =  {len(following)}\nfollowers = {len(followers)}\ndiff = {len(res)}')
print(res)


def write_data_to_file(data: list, filename: str):
    with open(filename, 'a') as file:
        for line in data:
            file.write(line + '\n')


write_data_to_file(followers, 'followers.txt')
write_data_to_file(following, 'following.txt')
write_data_to_file(diff, 'unfollowers')


def get_list_from_file(filename: str):
    with open('file.txt', 'r') as file:
        usernames = [line.strip() for line in file]
        return usernames


usernames_from_file = get_list_srom_file('unfollowers.')
print(set(usernames_from_file))