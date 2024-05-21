# Countries

<h3>General notes:</h3>

Numpy, Pandas, Matplotlib exercise. Using a web service in order to perform data analysis. Gap Minder data was used in order to create a composite index which is supposed to reflect ranking of countries by life quality.

Data was joined using outer join (more data points, less stability) and inner join (fewer data points, more stability) because not all data was available for all index components for every country.

The ranking is mostly irrelevant due to the nature of the data and the bias of the researcher in choosing categories and weighting (all arbitrary, no polling or reliability checking was done beforehand).

Emphasis is put on the structure of the approach and the shape of the result rather than on the numbers themselves.

<h3>Notes about index structure:</h3>

+ <h4> index composition</h4>

	index is comprised from 10 components, where each consists of 4 sub-components:

	<b>01. COMMUNICATION</b>
	<br>> fixed lines subscribers / 100 people
	<br>> cell phones / 100 people
	<br>> broadband subscribers / 100 people
	<br>> personal computers / 100 people

    <b>02. EDUCATION</b>
    <br>> literacy rate
    <br>> primary school completion rate
    <br>> females to males literacy ratio
    <br>> govt expenditure per student

    <b>03. ECONOMICS</b>
    <br>> GDP per capita, as index
    <br>> inflation, as index
    <br>> investments, %GDP
    <br>> trade balance, %GDP

    <b>04. ENVIRONMENT</b>
    <br>> material footprint per capita
    <br>> CO2 emissions per capita
    <br>> levels of water stress
    <br>> sustainable development index

    <b>05. INFRASTRUCTURE</b>
    <br>> 4-wheeled vehicels / 1000 people
    <br>> access to electricity, % pop
    <br>> access to sanitation, % pop
    <br>> access to water source, % pop

    <b>06. HEALTH</b>
    <br>> life expectancy at birth
    <br>> medical doctors / 1000 people
    <br>> total health spending, % GDP
    <br>> universal health coverage index

    <b>07. ENERGY</b>
    <br>> energy use per capita, kg of oil eq
    <br>> energy import, % tot
    <br>> alternative and nuclear energy, % tot
    <br>> renewable energy consumption, % tot

    <b>08. WORK</b>
    <br>> employment rate
    <br>> employment to population ratio
    <br>> ease of doing business
    <br>> total tax and contribution rate, % profit

    <b>09. SOCIETY</b>
    <br>> GINI coefficient
    <br>> perceived progress
    <br>> happiness score, WHR
    <br>> human development index, HDI

    <b>10. GOVERNMENT</b>
    <br>> democracy score
    <br>> civil liberties index, FH
    <br>> political rights index, FH
    <br>> corruption perception index

+ <h4> component weighting</h4>

    Data was normalized in order to get scores in %, with inverting where neccessary, and weighted per index subcomponent so score per component is obtained. Total scores were then weighted and summed over in order to obtain the final score.
    
    This was done for 3 categories of subjects: young people starting work, couples with small children and pensioners. Weights per index component were adjusted according to level of interest of the subject group for the life quality aspect in question.

+ <h4> stacked data plotting</h4>

	The composite index was plotted using hbar stacked plot and sorted by total score in order to obtain a representation of the data where it is visible how each component affects the total score per country.