"""Command line interface for the HexMazeInterface."""
import click
import os

from .hex_maze_interface import HexMazeInterface, MazeException


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = HexMazeInterface(debug=False)

@cli.command()
@click.pass_obj
def discover(hmi):
    cluster_addresses = hmi.discover_cluster_addresses()
    print(cluster_addresses)

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def check(hmi, cluster_address):
    communicating = hmi.check(cluster_address)
    print(communicating)

@cli.command()
@click.pass_obj
def check_all(hmi):
    communicating = hmi.check_all()
    print(communicating)

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def no_cmd(hmi, cluster_address):
    if hmi.no_cmd(cluster_address):
        print('no command received proper error response')
    else:
        print('no command did not receive proper error response!')

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def bad_cmd(hmi, cluster_address):
    if hmi.bad_cmd(cluster_address):
        print('bad command received proper error response')
    else:
        print('bad command did not receive proper error response!')

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def reset(hmi, cluster_address):
    hmi.reset(cluster_address)
    print('resetting')

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.argument('duration-ms', nargs=1, type=int)
@click.pass_obj
def beep(hmi, cluster_address, duration_ms):
    hmi.beep(cluster_address, duration_ms)

@cli.command()
@click.argument('duration-ms', nargs=1, type=int)
@click.pass_obj
def beep_all(hmi, duration_ms):
    hmi.beep_all(duration_ms)

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def led_off(hmi, cluster_address):
    hmi.led_off(cluster_address)

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def led_on(hmi, cluster_address):
    hmi.led_on(cluster_address)

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def led_on_then_off(hmi, cluster_address):
    hmi.led_on_then_off(cluster_address)

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.argument('repeat-count', nargs=1, type=int)
@click.pass_obj
def measure(hmi, cluster_address, repeat_count):
    duration = hmi.measure_communication(cluster_address, repeat_count)
    print('duration = ', duration)

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def power_off(hmi, cluster_address):
    hmi.power_off(cluster_address)

@cli.command()
@click.pass_obj
def power_off_all(hmi):
    hmi.power_off_all()

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def power_on(hmi, cluster_address):
    hmi.power_on_all(cluster_address)

@cli.command()
@click.pass_obj
def power_on_all(hmi):
    hmi.power_on_all()

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def home(hmi, cluster_address):
    hmi.home(cluster_address)

@cli.command()
@click.pass_obj
def home_all(hmi):
    hmi.home_all()

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.argument('positions-mm', nargs=HexMazeInterface.PRISM_COUNT, type=int)
@click.pass_obj
def write_target_positions(hmi, cluster_address, positions_mm):
    hmi.write_target_positions(cluster_address, positions_mm)

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def pause(hmi, cluster_address):
    hmi.pause(cluster_address)

@cli.command()
@click.pass_obj
def pause_all(hmi):
    hmi.pause_all()

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def resume(hmi, cluster_address):
    hmi.resume(cluster_address)

@cli.command()
@click.pass_obj
def resume_all(hmi):
    hmi.resume_all()

@cli.command()
@click.argument('cluster-address', nargs=1, type=int)
@click.pass_obj
def read_actual_positions(hmi, cluster_address):
    actual_positions = hmi.read_actual_positions(cluster_address)
    print(actual_positions)

