
import numpy
import matplotlib
matplotlib.rcParams['text.usetex'] = False

import matplotlib.pyplot as plt  # noqa

__all__ = ['plotall', 'plotonewithurls']


def plotall(df, max_nrows, max_ncols, max_figsize, **kwargs):
    """
    Plot fact/fake series for all stories in a grid, optionally spanning
    multiple pages if needed.

    Arguments
    =========
    max_nrows, max_ncols : int
        Maximum number of rows/columns of the subplots per page

    max_figsize : tuple
        A (width, height) tuple specifying the maximum size of a plot per page.

    Additional keyword arguments are passed to the plot of method of each data
    frame
    """
    plots_per_page = max_nrows * max_ncols
    keys = list(df.index.get_level_values(0).unique())
    n_subplots_tot = len(keys)
    max_width, max_height = max_figsize
    w_subplot = max_width / max_ncols
    h_subplot = max_height / max_nrows
    for i in range(0, n_subplots_tot, plots_per_page):
        j = i + plots_per_page
        keys_to_plot = keys[i:j]
        n_subplots = len(keys_to_plot)
        if n_subplots < n_subplots_tot:
            # adjust number of columns, rows and figsize based on n_subplots
            nrows = int(numpy.ceil(n_subplots / max_ncols))
            if nrows == 1:
                ncols = n_subplots
            else:
                ncols = max_ncols
            width = ncols * w_subplot
            height = nrows * h_subplot
            figsize = (width, height)
        else:
            # use maximum number of rows, colors, and figsize
            nrows = max_nrows
            ncols = max_ncols
            figsize = max_figsize

        subplots_kwargs = dict(nrows=nrows, ncols=ncols,
                               figsize=figsize)

        fig, axs = plt.subplots(**subplots_kwargs)

        for k, ax in zip(keys_to_plot, numpy.ravel(axs)):
            ts = df.loc[k].set_index('timestamp')
            t0 = ts.index[0].date()
            ts = ts.reset_index(drop=True)
            ts.plot(ax=ax, color=['gray', 'black'], legend=False, **kwargs)
            ax.set_xlabel('')
            ax.set_title("${}$".format(k))
            ymin, ymax = ax.get_ylim()
            ax.set_ylim(ymin, ymax + 0.25 * (ymax - ymin))
            ax.text(0.5, 0.85, "$t_0=$ {}".format(t0),
                    transform=ax.transAxes, horizontalalignment='center')

        # put legend on first plot
        axs = numpy.atleast_2d(axs)
        axs[0, 0].legend(frameon=False, loc='best')

        # subplots axis label (requires matplotlib 3.4.0+)
        fig.supxlabel('Hours since $t_0$', fontsize='x-large')
        fig.supylabel('Active Users', fontsize='x-large')

        # delete any unused subplot
        for ax in axs.ravel()[n_subplots:]:
            fig.delaxes(ax)

        # set tight layout
        plt.tight_layout(pad=0.2)
        path = f"allstories-{i}-{j-1}.pdf"
        plt.savefig(path)
        print(f"Written: {path}")
        plt.show()


# TODO:
# 1. Add legend >> Done
# 2. Split plot in two for fact/fake and remove log scale? Or plot fact-checks
#    on a second y-axis? >> Done
# 3. Can integrate in plotall so that plotall takes whatever plotting task one
#    wants? >> ???


def plotonewithurls(df, k):
    t0 = df.index[0]
    df = df.reset_index(drop=True)

    # fig = plt.gcf()
    # ax = plt.gca()

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    title = "Story " + str(k) + ": $t_0=$ {}".format(t0)
    fig.suptitle(title)

    ax1 = plt.subplot(1, 3, 1)
    df['fake'].plot(legend=False, color='b', ls='--', ax=ax1,
                    title="Fake news")
    ax1.set_yscale('symlog')
    ymin, ymax = ax1.get_ylim()
    ax1.set_ylim(ymin, ymax * 10)
    ax1.set_xlabel('Hours since $t_0$')
    ax1.set_ylabel('Active Users')
    ax2 = plt.subplot(1, 3, 2)
    df['fact'].plot(legend=False, color='r', ls='--', ax=ax2,
                    title="Fact-check")
    ax2.set_yscale('symlog')
    ymin, ymax = ax2.get_ylim()
    ax2.set_ylim(ymin, ymax * 10)
    ax2.set_xlabel('Hours since $t_0$')

    # ax3 = plt.subplot(1, 3, 3)
    # df['fake'].sum(axis=1).plot(legend=False, color='b', ls='-', ax=ax3,
    # label='fake')
    # df['fact'].sum(axis=1).plot(legend=False, color='r', ls='-', ax=ax3,
    # label='fact') ax3.set_title("Total")
    # ax3.set_yscale('symlog')
    # ymin, ymax = ax3.get_ylim()
    # ax3.set_ylim(ymin, ymax * 10)
    # ax3.set_xlabel('Hours since $t_0$')
    # ax3.legend(loc='best')

    ax3 = plt.subplot(1, 3, 3)
    df['fake'].sum(axis=1).plot(legend=False, color='b', ls='-', ax=ax3,
                                label='fake')
    ax3.set_ylabel('Fake Sharing', color='b')
    ax3.set_title("Total")
    ax3.set_yscale('symlog')
    ymin, ymax = ax3.get_ylim()
    ax3.set_ylim(ymin, ymax * 10)
    ax3.set_xlabel('Hours since $t_0$')
    ax4 = ax3.twinx()
    df['fact'].sum(axis=1).plot(legend=False, color='r', ls='-', ax=ax4,
                                label='fact')
    ax4.set_ylabel('Fact Sharing', color='r')
    ax4.tick_params('y', colors='r')

    plt.subplots_adjust(top=0.88)
    plt.tight_layout()

    plt.show()
