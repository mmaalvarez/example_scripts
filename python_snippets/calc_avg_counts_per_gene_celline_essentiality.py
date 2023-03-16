from statistics import mean

path = "/g/strcombio/fsupek_data/users/malvarez/crispr_screening/qc_ess_noness_nontarg/"
input_path = path +"2_counts/"
output_path = path +"3_avg_counts_sgRNA_per_gene_per_celline_per_essentiality/"

# create dictionary of counts:
# {essentiality1: {cell_line1: {gene1: ([counts_sgRNA1, ..., sgRNA4], average_counts), ...}, ...}, ...}
master_dict = dict()
for essentiality in ["essential", "nonessential"]:
    master_dict[f'{essentiality}'] = dict()
    with open(f'{input_path}{essentiality}_counts.txt', "r") as file:
        for i, line in enumerate(file):
            splitted_line = line.split("\t")
            if i == 0:
                header = splitted_line
                for head in header[2:]:
                    master_dict[f'{essentiality}'][head] = dict()
            else:
                gene = splitted_line[1]
                try:
                    # gene previously included
                    master_dict[f'{essentiality}']["LXF_289_wt_t0"][gene]
                except KeyError:
                    # new gene within a list, where the 2nd element is where the average will go
                    for cell_line in list(master_dict[f'{essentiality}'].keys()):
                        master_dict[f'{essentiality}'][cell_line][gene] = [[], 0]
                # append counts of the current gene's sgRNA to each cell line
                for i, cell_line in enumerate(list(master_dict[f'{essentiality}'].keys())):
                    cell_line_counts = int(splitted_line[2 + i])
                    master_dict[f'{essentiality}'][cell_line][gene][0].append(cell_line_counts)

# calculate averages
for essentiality in ["essential", "nonessential"]:
    for cell_line in master_dict[essentiality]:
        for gene in master_dict[essentiality][cell_line]:
            sgRNAs_counts = master_dict[essentiality][cell_line][gene][0]
            avg_counts = mean(sgRNAs_counts)
            master_dict[essentiality][cell_line][gene][1] = avg_counts


# print output
for essentiality in ["essential", "nonessential"]:
    with open(f'{output_path}{essentiality}_avg_counts.txt', "w") as out:
        for cell_line in master_dict[essentiality]:
            newline = [cell_line.strip()]
            for gene in master_dict[essentiality][cell_line]:
                gene_average = master_dict[essentiality][cell_line][gene][1]
                newline.append(str(gene_average))
            out.write("\t".join(newline) + "\n")
