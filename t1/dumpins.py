import pickle

fi=open("inserts.pickle", "rb")
fi2=open("inserts.sql", "w")

insets=pickle.load(fi)
fi.close()
for insert in insets:
    print(insert, file=fi2)
fi.close()