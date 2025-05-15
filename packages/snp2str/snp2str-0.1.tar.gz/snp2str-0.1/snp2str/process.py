import csv
import json
import os
from collections import OrderedDict
import pandas as pd
from snp2str.exceptions import InputError
from collections import Counter

def process_files(ped_path: str,
                  pop_path: str = None,
                  map_path: str = None,
                  add_header: bool = True,
                  output_path: str = "output.txt",
                  skip_input_header: bool = False) -> None:
    """

    :param ped_path: Path to the .ped file
    :param pop_path: Path to the population file (optional)
    :param map_path: Path to the .map file (optional)
    :param add_header: Whether to add a header to the output file
    :param output_path: Path for the output file
    :param skip_input_header: Whether to skip the first line in the .ped input file
    :return: None
    """

    if not output_path:
        output_path = "output.txt"

    with open(os.path.join(os.path.dirname(__file__), 'bases_coding.json')) as file:
        bases_coding = json.load(file)

    if map_path:
        header = pd.read_csv(map_path, sep="\t", header=None)[1].values.tolist()
    else:
        print("map_path not specified. Proceeding without header file.")
        header = None

    if pop_path:
        populations = pd.read_csv(pop_path, header=None)[0].tolist()
    else:
        print("pop_path not specified. Proceeding without populations file.")
        populations = None

    sequences = OrderedDict()

    with open(ped_path) as file:
        lines = file.readlines()
        # Skip the first line if skip_input_header is True
        start_line = 1 if skip_input_header else 0
        
        if skip_input_header and len(lines) > 0:
            print(f"Skipping first line in .ped file: {lines[0].strip()}")
            
        for line in lines[start_line:]:
            elements = line.split()
            cultivar_name = elements[1]
            sequence = elements[6:]
            sequences[cultivar_name] = list(map(lambda x: bases_coding[x], sequence))

    n_bases_set = set([len(val) for val in sequences.values()])
    n_bases = next(iter(n_bases_set))

    species_n_bases = {species: len(sequence) for species, sequence in sequences.items()}
    n_bases_mode = Counter(species_n_bases.values()).most_common(1)[0][0]
    species_not_mode = [species for species, n_bases in species_n_bases.items() if n_bases != n_bases_mode]

    if species_not_mode:
        raise InputError(f"The following species: {species_not_mode} have a different number of bases than the mode ({n_bases_mode}). Ensure the species name is correct and does not contain any extra spaces.")

    assert len(n_bases_set) == 1, f"Not all species have the same number of bases! Numbers: {n_bases_set}"

    print("Parsed %i species with %i bases each" % (len(sequences), n_bases))

    if header:
        assert len(header) == n_bases / 2, "Header size %s does not correspond with chromosome count %s" % (len(header), n_bases / 2)

    if populations:
        assert len(sequences) == len(populations), "Population number does not correspond"

    with open(output_path, "w") as file:
        writer = csv.writer(file, delimiter=" ")
        # write header
        if header and add_header:
            writer.writerow([None, None] + header)
        if header and not add_header:
            print("Header was present but add_header is False. Producing output without header.")
        # write each line
        for i, species in enumerate(sequences):
            strand1 = sequences[species][::2]
            strand2 = sequences[species][1::2]

            if len(strand1) != len(strand2):
                print(f"WARNING: Species '{species}' has unequal strand lengths: {len(strand1)} and {len(strand2)}")

            assert len(strand1) == len(strand2), "The two strands contain an unequal number of elements! %i and %i" % (len(strand1), len(strand2))

            if populations:
                row1 = [species, populations[i], *strand1]
                row2 = [species, populations[i], *strand2]
            else:
                row1 = [species, *strand1]
                row2 = [species, *strand2]

            writer.writerow(row1)
            writer.writerow(row2)

    print("Output saved at: %s" % os.path.abspath(output_path))
