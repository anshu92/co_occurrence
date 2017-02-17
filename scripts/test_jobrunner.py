######################################################
#
# unit tests for jobrunner
# written by Anshuman Sahoo (anshuman264@gmail.com)
#
######################################################
import random
import jobrunner


def test_retrieve():
    files = ['3853869', '4159784', '2766270', '4657330', '3727923']
    chosen_filename = random.choice(files)
    file = jobrunner.retrieve(chosen_filename)
    assert file is not None


def test_count_co_occurrences():
    sample_input = ('test', [1, 2, 3, 4])
    output = jobrunner.count_co_occurences(sample_input)
    assert output[1] == 10
