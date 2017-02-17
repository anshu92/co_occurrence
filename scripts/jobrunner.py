######################################################
#
# jobrunner - Runs the mapreduce jobs reducer function
# written by Anshuman Sahoo (anshuman264@gmail.com)
#
######################################################
import urllib.request
import xml.etree.ElementTree as ET
import operator
import json
import csv
import collections

from mapper_and_reducer import MapperAndReducer


def retrieve(filename):
    """
    Read a file and return a sequence of (word, occurrences) values.

    Parameters
    ----------
    filename : str
      PCMID to retrieve xml file

    Returns
    -------
    list
      List of tuples containing word and occurrences
    """

    ncbi_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id="

    data = urllib.request.urlopen(ncbi_url + filename).read()

    # Create a Element tree from the xml string retrieved
    root = ET.fromstring(data)

    # Get all the text in body
    body = root.find('.//body')
    if not body:
        return {'pmcid': filename, 'figures': None}

    body_text = ""
    for t in body.itertext():
        body_text += t

    # Find all the figure elements in the tree
    figures = root.findall('.//fig')

    # Go to next article if no figures are found
    if not figures:
        return {'pmcid': filename, 'figures': None}

    # Create a dictionary to store the co-occurence of each figure
    output = []
    ignore_words = {'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in', 'is', 'it', 'of', 'or', 'py', 'that',
                    'the', 'to', 'with', '', 'were', 'was', '=', 'The', 'from', 'at', 'on', 'using', 'after', '<', '>',
                    '1', 'not'}

    # Iterate through all figures in document and find co-occurrences between figure caption and article body.
    # Co-occurrence is defined such that, given a figure caption <F> and body text <B>, list the words that occur
    # in both <F> and <B>, and the number of co-occurrences
    for fig in figures:
        caption = ""
        caption_element = fig.find('.//caption')
        if caption_element is not None:
            for t in caption_element.itertext():
                caption += t

            list_of_figure_words = caption.split()
            list_of_body_words = body_text.split()

            for word in list_of_figure_words:
                if word not in ignore_words:
                    output.append((filename + '_' + word, list_of_body_words.count(word)))

            graphic = fig.find('.//graphic')
            figure_url = graphic.get('{http://www.w3.org/1999/xlink}href')

    print("Processed " + filename + "...")

    return output


def count_co_occurences(item):
    """
    Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    Parameters
    ----------
    item : tuple
      get a word occurence pair
    Returns
    -------
    list
      List of tuples containing word and occurrences
    """

    word, occurrences = item
    return (word.replace('.', '_dot_').replace('$', '_dol_'), sum(occurrences))


if __name__ == '__main__':
    # Skip first line of pmcids.txt because it is the title
    f = open('../data/pmcids.txt', 'r')
    first_line = f.readline()

    input_files = []
    while first_line:
        first_line = f.readline()[:-1]
        if len(first_line) > 1:
            input_files.append(first_line)
    f.close()

    mapper = MapperAndReducer(retrieve, count_co_occurences)
    word_counts = mapper(input_files)

    final_data = []

    for file in input_files:
        final_data.append({'pmcid': file, 'co_table': [(key[8:], value) for key, value in word_counts if key.startswith(file)]})

    # Store the generated table in a csv and json file
    file_name = "../output/co_occurrence_per_article"
    with open(file_name + ".json", 'w') as fp:
        json.dump(final_data, fp)

    with open(file_name + ".csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for word in word_counts:
            writer.writerow([word[0].encode('utf-8'), word[1]])


