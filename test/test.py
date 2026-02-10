"""Test CRM upload process"""
import test_mod_one as tmo


def main():

    t_one = tmo.TestCodeOne(pause=1)

    t_one.path_one()

    print("Done!")

    # TODO: Inline and inplace animation (e.g. hour glass)
    # TODO: Parameterize the symbol inbetween inline steps.


if __name__ == "__main__":
    main()
