import sys
sys.path.append('.')
from v2.rl.cnn.cnn import get_cnn_model
from achtung_tests.test import read_and_show_graph, test_and_save

if __name__ == '__main__':
    # test_and_save((get_cnn_model(), 'cnn_v2'))
    read_and_show_graph('cnn_v2')
