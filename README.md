
# AxelrodExamples

Strategy visualizations and example tournaments for the iterated
[Prisoner's Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma)
library [Axelrod](https://github.com/Axelrod-Python).


Strategy Visualizations
=======================

The first strategy visualization displays how often a strategy cooperates with
every other strategy per round, averaged over many interactions (~200
repeated games between every pair of strategies).

Cooperation Rate Heatmaps
-------------------------

<b>ZDGTFT2</b><br/>

<div style="text-align:center">
<p>Left: no noise | Right: 5% noise</p>
<img src ="http://www.marcharper.codes/axelrod/heatmaps/cooperation/ZD-GTFT-2: 0.25, 0.5.png" width="45%" alt="Cooperation Rate Heatmap"/>
<img src ="http://www.marcharper.codes/axelrod/heatmaps/cooperation-noisy/ZD-GTFT-2: 0.25, 0.5.png" width="45%" alt="Cooperation Rate Heatmap with 5% noise"/>
</div>

<b>Calculator</b><br/>

<div style="text-align:center">
<p>Left: no noise | Right: 5% noise</p>
<img src ="http://www.marcharper.codes/axelrod/heatmaps/cooperation/Calculator.png" width="45%" alt="Cooperation Heatmap"/>
<img src ="http://www.marcharper.codes/axelrod/heatmaps/cooperation-noisy/Calculator.png" width="45%" alt="Cooperation Heatmap with 5% noise"/>
</div>

As you can see, the introduction of noise alters the efficacy of Calculator's
cycle detection algorithm.

Average Score Heatmaps
----------------------

We can also visualize the average payoff per round earned by each strategy
versus every other strategy per round, averaged over many interactions (~200
repeated games between every pair of strategies).

<b>Alternator</b><br/>

<div style="text-align:center">
<p>Left: no noise | Right: 5% noise</p>
<img src ="http://www.marcharper.codes/axelrod/heatmaps/score/Alternator.png" width="45%" alt="Average Score Heatmap"/>
<img src ="http://www.marcharper.codes/axelrod/heatmaps/score-noisy/Alternator.png" width="45%" alt="Average Score Heatmap with 5% noise"/>
</div>

<b>Evolved ANN 5 Noise 05</b><br/>

Mean Score Heatmap
******************

<div style="text-align:center">
<p>Left: no noise | Right: 5% noise</p>
<img src ="http://www.marcharper.codes/axelrod/heatmaps/score/Evolved ANN 5 Noise 05.png" width="45%" alt="Mean Score Heatmap"/>
<img src ="http://www.marcharper.codes/axelrod/heatmaps/score-noisy/Evolved ANN 5 Noise 05.png" width="45%" alt="Mean Score Heatmap with 5% noise"/>
</div>


All Strategies Heatmaps
-----------------------

Click to see all the renderings for each strategy.

* [$\phi$](/strategies/$\phi$.md)
* [$\pi$](/strategies/$\pi$.md)
* [$e$](/strategies/$e$.md)
* [ALLCorALLD](/strategies/ALLCorALLD.md)
* [Adaptive](/strategies/Adaptive.md)
* [Adaptive Pavlov 2006](/strategies/Adaptive%20Pavlov%202006.md)
* [Adaptive Pavlov 2011](/strategies/Adaptive%20Pavlov%202011.md)
* [Adaptive Tit For Tat: 0.5](/strategies/Adaptive%20Tit%20For%20Tat:%200.5.md)
* [Aggravater](/strategies/Aggravater.md)
* [Alexei: ('D',)](/strategies/Alexei:%20('D',).md)
* [Alternator](/strategies/Alternator.md)
* [Alternator Hunter](/strategies/Alternator%20Hunter.md)
* [Anti Tit For Tat](/strategies/Anti%20Tit%20For%20Tat.md)
* [AntiCycler](/strategies/AntiCycler.md)
* [Appeaser](/strategies/Appeaser.md)
* [Arrogant QLearner](/strategies/Arrogant%20QLearner.md)
* [Average Copier](/strategies/Average%20Copier.md)
* [BackStabber: ('D', 'D')](/strategies/BackStabber:%20('D',%20'D').md)
* [Better and Better](/strategies/Better%20and%20Better.md)
* [Bully](/strategies/Bully.md)
* [Calculator](/strategies/Calculator.md)
* [Cautious QLearner](/strategies/Cautious%20QLearner.md)
* [Champion](/strategies/Champion.md)
* [CollectiveStrategy](/strategies/CollectiveStrategy.md)
* [Contrite Tit For Tat](/strategies/Contrite%20Tit%20For%20Tat.md)
* [Cooperator](/strategies/Cooperator.md)
* [Cooperator Hunter](/strategies/Cooperator%20Hunter.md)
* [Cycle Hunter](/strategies/Cycle%20Hunter.md)
* [Cycler CCCCCD](/strategies/Cycler%20CCCCCD.md)
* [Cycler CCCD](/strategies/Cycler%20CCCD.md)
* [Cycler CCCDCD](/strategies/Cycler%20CCCDCD.md)
* [Cycler CCD](/strategies/Cycler%20CCD.md)
* [Cycler DC](/strategies/Cycler%20DC.md)
* [Cycler DDC](/strategies/Cycler%20DDC.md)
* [DBS: 0.75, 3, 4, 3, 5](/strategies/DBS:%200.75,%203,%204,%203,%205.md)
* [Davis: 10](/strategies/Davis:%2010.md)
* [Defector](/strategies/Defector.md)
* [Defector Hunter](/strategies/Defector%20Hunter.md)
* [Desperate](/strategies/Desperate.md)
* [DoubleCrosser: ('D', 'D')](/strategies/DoubleCrosser:%20('D',%20'D').md)
* [DoubleResurrection](/strategies/DoubleResurrection.md)
* [Doubler](/strategies/Doubler.md)
* [Dynamic Two Tits For Tat](/strategies/Dynamic%20Two%20Tits%20For%20Tat.md)
* [EasyGo](/strategies/EasyGo.md)
* [Eatherley](/strategies/Eatherley.md)
* [EugineNier: ('D',)](/strategies/EugineNier:%20('D',).md)
* [Eventual Cycle Hunter](/strategies/Eventual%20Cycle%20Hunter.md)
* [Evolved ANN](/strategies/Evolved%20ANN.md)
* [Evolved ANN 5](/strategies/Evolved%20ANN%205.md)
* [Evolved ANN 5 Noise 05](/strategies/Evolved%20ANN%205%20Noise%2005.md)
* [Evolved FSM 16](/strategies/Evolved%20FSM%2016.md)
* [Evolved FSM 16 Noise 05](/strategies/Evolved%20FSM%2016%20Noise%2005.md)
* [Evolved FSM 4](/strategies/Evolved%20FSM%204.md)
* [Evolved HMM 5](/strategies/Evolved%20HMM%205.md)
* [EvolvedLookerUp1_1_1](/strategies/EvolvedLookerUp1_1_1.md)
* [EvolvedLookerUp2_2_2](/strategies/EvolvedLookerUp2_2_2.md)
* [Feld: 1.0, 0.5, 200](/strategies/Feld:%201.0,%200.5,%20200.md)
* [Firm But Fair](/strategies/Firm%20But%20Fair.md)
* [Fool Me Forever](/strategies/Fool%20Me%20Forever.md)
* [Fool Me Once](/strategies/Fool%20Me%20Once.md)
* [Forgetful Fool Me Once: 0.05](/strategies/Forgetful%20Fool%20Me%20Once:%200.05.md)
* [Forgetful Grudger](/strategies/Forgetful%20Grudger.md)
* [Forgiver](/strategies/Forgiver.md)
* [Forgiving Tit For Tat](/strategies/Forgiving%20Tit%20For%20Tat.md)
* [Fortress3](/strategies/Fortress3.md)
* [Fortress4](/strategies/Fortress4.md)
* [GTFT: 0.33](/strategies/GTFT:%200.33.md)
* [General Soft Grudger: n=1,d=4,c=2](/strategies/General%20Soft%20Grudger:%20n=1,d=4,c=2.md)
* [Gradual](/strategies/Gradual.md)
* [Gradual Killer: ('D', 'D', 'D', 'D', 'D', 'C', 'C')](/strategies/Gradual%20Killer:%20('D',%20'D',%20'D',%20'D',%20'D',%20'C',%20'C').md)
* [Grofman](/strategies/Grofman.md)
* [Grudger](/strategies/Grudger.md)
* [GrudgerAlternator](/strategies/GrudgerAlternator.md)
* [Grumpy: Nice, 10, -10](/strategies/Grumpy:%20Nice,%2010,%20-10.md)
* [Handshake](/strategies/Handshake.md)
* [Hard Go By Majority](/strategies/Hard%20Go%20By%20Majority.md)
* [Hard Go By Majority: 10](/strategies/Hard%20Go%20By%20Majority:%2010.md)
* [Hard Go By Majority: 20](/strategies/Hard%20Go%20By%20Majority:%2020.md)
* [Hard Go By Majority: 40](/strategies/Hard%20Go%20By%20Majority:%2040.md)
* [Hard Go By Majority: 5](/strategies/Hard%20Go%20By%20Majority:%205.md)
* [Hard Prober](/strategies/Hard%20Prober.md)
* [Hard Tit For 2 Tats](/strategies/Hard%20Tit%20For%202%20Tats.md)
* [Hard Tit For Tat](/strategies/Hard%20Tit%20For%20Tat.md)
* [Hesitant QLearner](/strategies/Hesitant%20QLearner.md)
* [Hopeless](/strategies/Hopeless.md)
* [Inverse](/strategies/Inverse.md)
* [Inverse Punisher](/strategies/Inverse%20Punisher.md)
* [Joss: 0.9](/strategies/Joss:%200.9.md)
* [Knowledgeable Worse and Worse](/strategies/Knowledgeable%20Worse%20and%20Worse.md)
* [Level Punisher](/strategies/Level%20Punisher.md)
* [Limited Retaliate 2: 0.08, 15](/strategies/Limited%20Retaliate%202:%200.08,%2015.md)
* [Limited Retaliate 3: 0.05, 20](/strategies/Limited%20Retaliate%203:%200.05,%2020.md)
* [Limited Retaliate: 0.1, 20](/strategies/Limited%20Retaliate:%200.1,%2020.md)
* [MEM2](/strategies/MEM2.md)
* [Math Constant Hunter](/strategies/Math%20Constant%20Hunter.md)
* [Naive Prober: 0.1](/strategies/Naive%20Prober:%200.1.md)
* [Negation](/strategies/Negation.md)
* [Nice Average Copier](/strategies/Nice%20Average%20Copier.md)
* [Nydegger](/strategies/Nydegger.md)
* [Omega TFT: 3, 8](/strategies/Omega%20TFT:%203,%208.md)
* [Once Bitten](/strategies/Once%20Bitten.md)
* [Opposite Grudger](/strategies/Opposite%20Grudger.md)
* [PSO Gambler 1_1_1](/strategies/PSO%20Gambler%201_1_1.md)
* [PSO Gambler 2_2_2](/strategies/PSO%20Gambler%202_2_2.md)
* [PSO Gambler 2_2_2 Noise 05](/strategies/PSO%20Gambler%202_2_2%20Noise%2005.md)
* [PSO Gambler Mem1](/strategies/PSO%20Gambler%20Mem1.md)
* [Predator](/strategies/Predator.md)
* [Prober](/strategies/Prober.md)
* [Prober 2](/strategies/Prober%202.md)
* [Prober 3](/strategies/Prober%203.md)
* [Prober 4](/strategies/Prober%204.md)
* [Pun1](/strategies/Pun1.md)
* [Punisher](/strategies/Punisher.md)
* [Raider](/strategies/Raider.md)
* [Random Hunter](/strategies/Random%20Hunter.md)
* [Random: 0.5](/strategies/Random:%200.5.md)
* [Remorseful Prober: 0.1](/strategies/Remorseful%20Prober:%200.1.md)
* [Resurrection](/strategies/Resurrection.md)
* [Retaliate 2: 0.08](/strategies/Retaliate%202:%200.08.md)
* [Retaliate 3: 0.05](/strategies/Retaliate%203:%200.05.md)
* [Retaliate: 0.1](/strategies/Retaliate:%200.1.md)
* [Revised Downing: True](/strategies/Revised%20Downing:%20True.md)
* [Ripoff](/strategies/Ripoff.md)
* [Risky QLearner](/strategies/Risky%20QLearner.md)
* [SelfSteem](/strategies/SelfSteem.md)
* [ShortMem](/strategies/ShortMem.md)
* [Shubik](/strategies/Shubik.md)
* [Slow Tit For Two Tats](/strategies/Slow%20Tit%20For%20Two%20Tats.md)
* [Slow Tit For Two Tats 2](/strategies/Slow%20Tit%20For%20Two%20Tats%202.md)
* [Sneaky Tit For Tat](/strategies/Sneaky%20Tit%20For%20Tat.md)
* [Soft Go By Majority](/strategies/Soft%20Go%20By%20Majority.md)
* [Soft Go By Majority: 10](/strategies/Soft%20Go%20By%20Majority:%2010.md)
* [Soft Go By Majority: 20](/strategies/Soft%20Go%20By%20Majority:%2020.md)
* [Soft Go By Majority: 40](/strategies/Soft%20Go%20By%20Majority:%2040.md)
* [Soft Go By Majority: 5](/strategies/Soft%20Go%20By%20Majority:%205.md)
* [Soft Grudger](/strategies/Soft%20Grudger.md)
* [Soft Joss: 0.9](/strategies/Soft%20Joss:%200.9.md)
* [SolutionB1](/strategies/SolutionB1.md)
* [SolutionB5](/strategies/SolutionB5.md)
* [Spiteful Tit For Tat](/strategies/Spiteful%20Tit%20For%20Tat.md)
* [Stalker: D](/strategies/Stalker:%20D.md)
* [Stein and Rapoport: 0.05: ('D', 'D')](/strategies/Stein%20and%20Rapoport:%200.05:%20('D',%20'D').md)
* [Stochastic Cooperator](/strategies/Stochastic%20Cooperator.md)
* [Stochastic WSLS: 0.05](/strategies/Stochastic%20WSLS:%200.05.md)
* [Suspicious Tit For Tat](/strategies/Suspicious%20Tit%20For%20Tat.md)
* [TF1](/strategies/TF1.md)
* [TF2](/strategies/TF2.md)
* [TF3](/strategies/TF3.md)
* [Tester](/strategies/Tester.md)
* [ThueMorse](/strategies/ThueMorse.md)
* [ThueMorseInverse](/strategies/ThueMorseInverse.md)
* [Thumper](/strategies/Thumper.md)
* [Tit For 2 Tats](/strategies/Tit%20For%202%20Tats.md)
* [Tit For Tat](/strategies/Tit%20For%20Tat.md)
* [Tricky Cooperator](/strategies/Tricky%20Cooperator.md)
* [Tricky Defector](/strategies/Tricky%20Defector.md)
* [Tullock: 11](/strategies/Tullock:%2011.md)
* [Two Tits For Tat](/strategies/Two%20Tits%20For%20Tat.md)
* [VeryBad](/strategies/VeryBad.md)
* [Willing](/strategies/Willing.md)
* [Win-Shift Lose-Stay: D](/strategies/Win-Shift%20Lose-Stay:%20D.md)
* [Win-Stay Lose-Shift: C](/strategies/Win-Stay%20Lose-Shift:%20C.md)
* [Winner12](/strategies/Winner12.md)
* [Winner21](/strategies/Winner21.md)
* [Worse and Worse](/strategies/Worse%20and%20Worse.md)
* [Worse and Worse 2](/strategies/Worse%20and%20Worse%202.md)
* [Worse and Worse 3](/strategies/Worse%20and%20Worse%203.md)
* [ZD-Extort-2 v2: 0.125, 0.5, 1](/strategies/ZD-Extort-2%20v2:%200.125,%200.5,%201.md)
* [ZD-Extort-2: 0.1111111111111111, 0.5](/strategies/ZD-Extort-2:%200.1111111111111111,%200.5.md)
* [ZD-Extort-4: 0.23529411764705882, 0.25, 1](/strategies/ZD-Extort-4:%200.23529411764705882,%200.25,%201.md)
* [ZD-GEN-2: 0.125, 0.5, 3](/strategies/ZD-GEN-2:%200.125,%200.5,%203.md)
* [ZD-GTFT-2: 0.25, 0.5](/strategies/ZD-GTFT-2:%200.25,%200.5.md)
* [ZD-SET-2: 0.25, 0.0, 2](/strategies/ZD-SET-2:%200.25,%200.0,%202.md)



Example Tournaments
===================

See the python script [example_tournaments.py](example_tournaments.py) for the
exact details of each tournament.

All Fair Strategies
-------------------

This tournament covers all strategies in the Axelrod library that follow the standard Axelrod rules.


Score Distributions
*******************

<div style="text-align:center">
<p>Left: no noise | Right: 5% noise</p>
<img src="http://www.marcharper.codes/axelrod/tournaments/AllFairStrategies/AllFairStrategies_boxplot.svg" width="45%"/>
<img src="http://www.marcharper.codes/axelrod/tournaments/AllFairStrategies-noise/AllFairStrategies-noise_boxplot.svg" width="45%"/>
</div>

Win Distributions
*****************

<div style="text-align:center">
<p>Left: no noise | Right: 5% noise</p>
<img src ="http://www.marcharper.codes/axelrod/tournaments/AllFairStrategies/AllFairStrategies_winplot.svg" width="45%"/>
<img src ="http://www.marcharper.codes/axelrod/tournaments/AllFairStrategies-noise/AllFairStrategies-noise_winplot.svg" width="45%"/>
</div>

Pairwise Payoffs
****************

<div style="text-align:center">
<p>Left: no noise | Right: 5% noise</p>
<img src ="http://www.marcharper.codes/axelrod/tournaments/AllFairStrategies/AllFairStrategies_payoff.svg" width="45%"/>
<img src ="http://www.marcharper.codes/axelrod/tournaments/AllFairStrategies-noise/AllFairStrategies-noise_payoff.svg" width="45%"/>
</div>


Tournaments
-----------

Click to see all the renderings for each tournament.



* [All Fair Strategies](tournaments/AllFairStrategies.md)
This tournament covers all strategies in the Axelrod library that follow the standard Axelrod rules.

* [Deterministic](tournaments/Deterministic.md)
All deterministic strategies.

* [Stochastic](tournaments/Stochastic.md)
All stochastic strategies.

* [Finite Memory](tournaments/FiniteMemory.md)
The players in this tournament are all strategies that remember a finite number of rounds (i.e. do not retain history indefinitely).

* [Memory One](tournaments/Memoryone.md)
The players in this tournament are all memoryone strategies (having memory depth 0 or 1).

* [Stewart & Plotkin 2012](tournaments/StewartPlotkin2012.md)
This tournament covers the same strategies in [Stewart and Plotkin's 2012 tournament](http://www.pnas.org/content/109/26/10134.full.pdf)

* [Tyler Singer-Clark](tournaments/tscizzle.md)
This tournament's players are those used in Tyler Singer-Clark's paper [Morality Metrics On Iterated Prisoner's Dilemma Players](http://www.scottaaronson.com/morality.pdf)

