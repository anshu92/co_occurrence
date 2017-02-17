######################################################
#
# retrieval - retrieve documents using pmcids and process it for co-occurrence
# Initial attempt to download and process data
# written by Anshuman Sahoo (anshuman264@gmail.com)
#
######################################################
import urllib.request
import xml.etree.ElementTree as ET
import json
import csv


def co_occurrence(f, b):
    """
    Given a list of words from the figure caption and the body text, return a table/dictionary
    containing words in caption (key) and their occurrence in body.
    Parameters
    ----------
    f : list
        list conatining words from figure caption
    b : str
        list containing words from body text

    Returns
    -------
    dict
        A key of words in figure and their cooccurences in body

    """
    list_of_figure_words = f.split()
    list_of_body_words = b.split()
    co_table = dict()
    for c in list_of_figure_words:
        if c != '':
            co_table[c.replace('.', '_dot_').replace('$', '_dol_')] = list_of_body_words.count(c)

    return co_table


def retrieval(url):
    """
    Retrieves xml document from ncbi database using pmcid code, saves it in an Element tree, parses
    it into lists of words for body and each figure. Then accumulate the counts.
    Extended description of function.

    Parameters
    ----------
    url : str
        database url for ncbi efetch

    Returns
    -------
    None
        writes outputs to file
    """
    # Skip first line of pmcids.txt because it is the title
    f = open('../data/pmcids.txt', 'r')
    first_line = f.readline()

    co_list = []

    while first_line:
        first_line = f.readline()[:-1]

        data = urllib.request.urlopen(url + first_line).read()

        # Create a Element tree from the xml string retrieved
        root = ET.fromstring(data)

        # Get all the text in body
        body = root.find('.//body')
        if not body:
            continue

        body_text = ""
        for t in body.itertext():
            body_text += t

        # Find all the figure elements in the tree
        figures = root.findall('.//fig')

        # Go to next article if no figures are found
        if not figures:
            continue

        # Create a dictionary to store the co-occurence of each figure
        fig_co_table = dict()

        # Iterate through all figures in document and find co-occurrences between figure caption and article body.
        # Co-occurrence is defined such that, given a figure caption <F> and body text <B>, list the words that occur
        # in both <F> and <B>, and the number of co-occurrences
        for fig in figures:
            caption = ""
            caption_element = fig.find('.//caption')
            if caption_element is not None:
                for t in caption_element.itertext():
                    caption += t

                co_table = co_occurrence(caption, body_text)

                graphic = fig.find('.//graphic')
                figure_url = graphic.get('{http://www.w3.org/1999/xlink}href')

                fig_co_table[figure_url.replace('.', '_dot_').replace('$', '_dol_')] = co_table

        co_list.append({'pmcid': first_line, 'figures': fig_co_table})
        print("Processed " + first_line + "...")

    # Store the generated table in a csv and json file
    file_name = "../output/co_occurrence"
    with open(file_name + ".json", 'w') as fp:
        json.dump(co_list, fp)

    for item in co_list:
        for fig_url, co_table in item['figures'].items():
            with open(file_name + ".csv", "w", newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                for word, occurrences in co_table.items():
                    writer.writerow([item['pmcid'], fig_url, word.encode('utf-8'), occurrences])

    f.close()


ncbi_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id="

if __name__ == '__main__':
    retrieval(ncbi_url)
