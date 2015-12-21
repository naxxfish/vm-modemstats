while [ 1 ]; do
echo "Getting Stats"
python get_vm_stats.py
echo "Updating Graphs"
python graph_vm_stats.py
sleep 30
done
