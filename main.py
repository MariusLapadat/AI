import time
import functions

if __name__ == '__main__':
    while True:
        print("1.Problema rucsacului cu algorit evolutiv")
        print("2.Problema TSP cu algoritm evolutiv")
        print("x.Iesire")

        optiune = input("Alegeti optiunea:")
        if optiune == "1":
            # pop_size = int(input("Introduceti numarul de indivizi ai populatiei:"))
            # num_gen = int(input("Introduceti numarul de generatii:"))
            # mut_chance = int(input("Introduceti sansa de mutatie"))
            for i in range(10):
                print(functions.evo_alg(500, 1000, 10))

        elif optiune == "2":
            # pop_size = int(input("Introduceti numarul de indivizi ai populatiei:"))
            # num_gen = int(input("Introduceti numarul de generatii:"))
            # mut_chance = int(input("Introduceti sansa de mutatie"))
            for i in range(10):
                functions.evo_alg_tsp(500, 500, 10)

        elif optiune == "x":
            break

    # random_list20 = generate20()
    # print(validate20(data_list,max_weight,random_list20))
