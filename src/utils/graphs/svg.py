import io
import base64

def fig_to_svg_base64(fig):
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='svg', bbox_inches='tight')
    svg_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return svg_b64
