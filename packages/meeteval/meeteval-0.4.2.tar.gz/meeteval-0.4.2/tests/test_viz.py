import meeteval.viz
from pathlib import Path
import pytest

example_files = (Path(__file__).parent.parent / 'example_files').absolute()


@pytest.mark.parametrize(
    'alignment',
    [
        'cp', 'tcp', 'orc', 'tcorc', 'greedy_tcorc',
        'greedy_orc', 'greedy_dicp', 'greedy_ditcp'
    ]
)
def test_viz_burn(alignment):
    """
    Tests if the code that generated the visualization produces an html file.
    Does not test if the visualization is correct.
    """
    ref = meeteval.io.asseglst(meeteval.io.load(example_files / 'hyp.stm')).groupby('session_id')
    hyp = meeteval.io.asseglst(meeteval.io.load(example_files / 'ref.stm')).groupby('session_id')

    for k in ref.keys():
        meeteval.viz.AlignmentVisualization(
            ref[k],
            hyp[k],
            alignment=alignment,
        ).dump(example_files / f'viz/test-{k}-{alignment}.html')
        assert (example_files / f'viz/test-{k}-{alignment}.html').exists()


@pytest.mark.parametrize(
    'alignment',
    [
        'cp', 'tcp', 'orc', 'tcorc', 'greedy_tcorc',
        'greedy_orc', 'greedy_dicp', 'greedy_ditcp'
    ]
)
def test_viz_precompute_wer(alignment):
    """
    Tests if the code that generated the visualization produces an html file
    when the WER (and assignment) are precomputed.
    Does not test if the visualization is correct.
    """
    ref = meeteval.io.asseglst(meeteval.io.load(example_files / 'hyp.stm')).groupby('session_id')
    hyp = meeteval.io.asseglst(meeteval.io.load(example_files / 'ref.stm')).groupby('session_id')

    for k in ref.keys():
        # Precompute WER
        wer = getattr(meeteval.wer.api, alignment + 'wer')(
            ref[k], hyp[k],
            **({'collar': 5} if 'tc' in alignment else {})
        )[k]

        # With precomputed WER
        meeteval.viz.AlignmentVisualization(
            ref[k],
            hyp[k],
            alignment=alignment,
            precomputed_error_rate=wer,
        ).dump(example_files / f'viz/test-{k}-{alignment}-precomputed.html')
        assert (example_files / f'viz/test-{k}-{alignment}-precomputed.html').exists()

        # Without precomputed WER
        meeteval.viz.AlignmentVisualization(
            ref[k],
            hyp[k],
            alignment=alignment,
        ).dump(example_files / f'viz/test-{k}-{alignment}.html')
        assert (example_files / f'viz/test-{k}-{alignment}.html').exists()

        # Test that file contents are identical. Only the (randomly generated)
        # visualization ID should differ.
        import re
        precomputed_text = (example_files / f'viz/test-{k}-{alignment}-precomputed.html').read_text()
        precomputed_text = re.sub(r'viz-[0-9a-f\-]*', '#viz-XXXX', precomputed_text)
        text = (example_files / f'viz/test-{k}-{alignment}.html').read_text()
        text = re.sub(r'viz-[0-9a-f\-]*', '#viz-XXXX', text)
        assert text == precomputed_text
