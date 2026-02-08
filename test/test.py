"""Test CRM upload process"""
import test_mod_one as tmo


def main():

    t_one = tmo.TestCodeOne(pause=1)

    t_one.path_one()

    print("Done!")


if __name__ == "__main__":
    main()
