# Do not modify these lines
__winc_id__ = 'd0d3cdcefbb54bc980f443c04ab3a9eb'
__human_name__ = 'operators'

# Add your code after this line

# Do this for the following statements, in this order:

#The language spoken the most in Switzerland is the same as in Spain.
most_spoken_language_switzerland = 'Swiss German'
most_spoken_language_spain = 'Castilian Spanish'

print(most_spoken_language_switzerland == most_spoken_language_spain)


#The most prevalent religion in Switzerland is the same as in Spain.
most_prevalent_religion_switzerland = 'Roman Catholic'
most_prevalent_religion_spain = 'Roman Catholic'

print(most_prevalent_religion_switzerland == most_prevalent_religion_spain)


#The name length of Spain's capital does not equal that of Switzerland.
capital_length_switzerland = len('bern')
capital_length_spain = len('madrid')

print(capital_length_switzerland != capital_length_spain)


#Switzerland's GDP is greater than Spain's GDP.
gdp_switzerland = 590710000000
gdp_spain = 1714860000000

print(gdp_switzerland > gdp_spain)


#The population growth is less than 1% in Switzerland and Spain.
population_growth_switzerland = 0.65/100
population_growth_spain = 0.13/100

print(population_growth_switzerland < 1/100 and population_growth_spain < 1 / 100)
#At least one of the two countries has a population count of over 10 million.
population_count_switzerland = 8508698
population_count_spain = 47163418
print(population_count_switzerland > 10000000 or population_count_spain > 10000000)
#Exactly one of the two countries has a population count of over 10 million.
print((population_count_switzerland > 10000000 or population_count_spain > 10000000) != (population_count_switzerland > 10000000 and population_count_spain > 10000000))
