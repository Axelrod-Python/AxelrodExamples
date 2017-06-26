
# Generate the data
python strategy_visualizations.py -d &
python strategy_visualizations.py -d -n 0.05 &
wait

# Strategy Visualizations
echo "Cooperation Visualizations, no noise (in background process)"
python strategy_visualizations.py -t 200 -r 100 -n 0.00 -f c &
echo "Opponent Cooperation Visualizations, no noise (in background process)"
python strategy_visualizations.py -t 200 -r 100 -n 0.00 -f oc &
echo "Score Visualizations, no noise (in background process)"
python strategy_visualizations.py -t 200 -r 100 -n 0.00 -f s &
echo "Score Difference Visualizations, no noise (in background process)"
python strategy_visualizations.py -t 200 -r 100 -n 0.00 -f sd &
wait

# Strategy Visualizations with Noise
echo "Cooperation Visualizations, 0.05 noise (in background process)"
python strategy_visualizations.py -t 200 -r 100 -n 0.05 -f c &
echo "Opponent Cooperation Visualizations, 0.05 noise (in background process)"
python strategy_visualizations.py -t 200 -r 100 -n 0.05 -f oc &
echo "Score Visualizations, 0.05 noise (in background process)"
python strategy_visualizations.py -t 200 -r 100 -n 0.05 -f s &
echo "Score Difference Visualizations, 0.05 noise (in background process)"
python strategy_visualizations.py -t 200 -r 100 -n 0.05 -f sd &
wait

# Noise-free Tournaments
echo "Small tournaments, no noise"
python example_tournaments.py -t 200 -r 100 -n 0.00 -p 4
echo "All strategies, no noise"
python example_tournaments.py -t 200 -r 100 -n 0.00 -p 4 -a
# Noisy Tournaments
echo "Small tournaments, 0.05 noise"
python example_tournaments.py -t 200 -r 100 -n 0.05 -p 4
echo "All strategies, 0.05 noise"
python example_tournaments.py -t 200 -r 100 -n 0.05 -p 4 -a

wait

python render_templates.py

echo "All tasks complete"
