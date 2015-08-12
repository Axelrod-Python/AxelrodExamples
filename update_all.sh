
# Noise-free Tournaments
echo "Small tournaments, no noise"
python example_tournaments.py -t 200 -r 500 -n 0.00 -p 8
echo "All strategies, no noise"
python example_tournaments.py -t 200 -r 100 -n 0.00 -p 8 -a
# Noisy Tournaments
echo "Small tournaments, 0.05 noise"
python example_tournaments.py -t 200 -r 500 -n 0.05 -p 8
echo "All strategies, 0.05 noise"
python example_tournaments.py -t 200 -r 100 -n 0.05 -p 8 -a

# Strategy Visualizations
echo "Cooperation Visualizations, no noise (in background process)"
python strategy_visualizations.py -t 200 -r 400 -n 0.00 -f c &
echo "Cooperation Visualizations, 0.05 noise (in background process)"
python strategy_visualizations.py -t 200 -r 400 -n 0.05 -f c &
echo "Strategy Visualizations, no noise (in background process)"
python strategy_visualizations.py -t 200 -r 400 -n 0.00 -f s &
echo "Strategy Visualizations, 0.05 noise (in background process)"
python strategy_visualizations.py -t 200 -r 400 -n 0.05 -f s &

wait
echo "All tasks complete"

# git commit -am "Update all assets"
# git push github master
