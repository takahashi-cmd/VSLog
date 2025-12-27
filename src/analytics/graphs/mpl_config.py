from matplotlib import font_manager
import matplotlib.pyplot as plt

_configured = False

def configure_matplotlib():
    """
    importされるたびにrcParamsをいじると副作用が出るので、
    初回だけ設定する。
    """
    global _configured
    if _configured:
        return
    
    # matplotlibのフォント定義
    font_path = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()

    # SVGグラフのフォントにテキストを埋め込み
    plt.rcParams['svg.fonttype'] = 'none'

    _configured = True
