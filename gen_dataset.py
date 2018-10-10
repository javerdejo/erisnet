"""Generates the modis dataset for training the neural network."""
import glob
import os
import h5py


def getProductsList(path):
    """Load the products list from a given path."""
    product_list = glob.glob(path + "/*")

    products = []
    for product in product_list:
        products.append(os.path.basename(product))

    products.sort()
    return products


def getProdPrefixes(modis_path, product):
    """Get the prefix of the file name for the products files."""
    file_list = glob.glob(modis_path + '/' + product + "/*")

    prefix_list = []
    for file in file_list:
        file_name = os.path.basename(file)
        prefix_list.append(file_name.split('.')[0])

    prefix_list.sort()
    return prefix_list


def get_file_name(modis_path, prefix, product):
    """Get the file name for a product and prefix given."""
    file_name = glob.glob(modis_path + '/' +
                          product + '/' +
                          prefix + '*')

    if file_name != []:
        return file_name[0]
    else:
        return None


def generate_product_dataset(modis_path, modis_list, prefix_list, filename):
    """Generate dataset."""
    dataset = []
    final_prefix = []

    for prefix in prefix_list:
        field_list = []
        for product in modis_list:
            file_name = get_file_name(modis_path, prefix, product)
            if file_name is not None:
                field_list.append(file_name)
            else:
                field_list = []
                break

        if len(field_list) != 0:
            dataset.append(field_list)
            final_prefix.append(prefix)

    return dataset, final_prefix


def extract_dataset(modis_path, dataset, modis_list, final_prefix, filename):
    """Extract dataset and save it in a h5 format file."""
    # If file exists returns a None object
    if os.path.isfile(filename):
        print ("Error: %s file exists" % (filename))
        return None

    # create h5 file
    f = h5py.File(filename, 'w')

    for product in modis_list:
        grp = f.create_group(product)

    f.close()


def main():
    """Define main function."""
    modis_path = "../modis"
    dataset_file_name = "../data.h5"
    modis_list = getProductsList(modis_path)
    prefix_list = getProdPrefixes(modis_path, modis_list[0])
    dataset, final_prefix = generate_product_dataset(modis_path,
                                                     modis_list,
                                                     prefix_list,
                                                     dataset_file_name)

    extract_dataset(modis_path,
                    dataset,
                    modis_list,
                    final_prefix,
                    dataset_file_name)


if __name__ == "__main__":
    main()
