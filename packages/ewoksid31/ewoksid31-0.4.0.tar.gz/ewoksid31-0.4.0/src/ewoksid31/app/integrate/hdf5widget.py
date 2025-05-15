from __future__ import annotations

import hdf5plugin  # noqa
import h5py

import silx.gui.hdf5
from silx.gui.hdf5._utils import H5Node
from silx.gui import qt
from silx.gui.data.DataViewerFrame import DataViewerFrame


class Hdf5TreeView(qt.QMainWindow):

    clicked = qt.Signal()

    def __init__(self):
        super().__init__()
        self.__loadedFiles: set[str] = set()

        self.__treeview = silx.gui.hdf5.Hdf5TreeView(self)
        self.__treeview.setSelectionMode(
            qt.QAbstractItemView.SelectionMode.ExtendedSelection
        )

        self.__dataViewer = DataViewerFrame(self)

        self.__treeview.setMinimumWidth(100)
        self.__dataViewer.setMinimumWidth(100)

        splitter = qt.QSplitter(self)
        splitter.addWidget(self.__treeview)
        splitter.addWidget(self.__dataViewer)

        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        splitter.setHandleWidth(10)
        splitter.setStretchFactor(1, 1)

        centralWidget = qt.QWidget(self)
        layout = qt.QVBoxLayout(centralWidget)
        layout.addWidget(splitter)

        self.setCentralWidget(centralWidget)

        self.__treeview.activated.connect(self.__displayData)
        self.__treeview.addContextMenuCallback(self.__closeAndSyncCustomContextMenu)
        self.__treeview.clicked.connect(self.clicked)

    def __displayData(self) -> None:
        """
        Update the data viewer with the currently selected HDF5 node.
        """
        selected = list(self.__treeview.selectedH5Nodes())
        if len(selected) >= 1:
            data = selected[-1]
            self.__dataViewer.setData(data)

    def addFile(self, filename: str) -> None:
        """
        Add a file to the HDF5 tree viewer.

        Prevents adding duplicate files by checking if the file is already loaded.

        Args:
            filename: Path to the HDF5 file to add.
        """
        if filename in self.__loadedFiles:
            qt.QMessageBox.information(
                self,
                "Duplicate File",
                f"This file {filename} is already loaded.",
            )
            return

        self.__treeview.findHdf5TreeModel().appendFile(filename)
        self.__loadedFiles.add(filename)

    def clearFiles(self) -> None:
        """
        Remove and close all files currently loaded in the HDF5 tree viewer.

        Resets the internal file tracking list.
        """
        self.__treeview.findHdf5TreeModel().clear()
        self.__loadedFiles.clear()

    def getLoadedFiles(self) -> set[str]:
        """
        Get the set of currently loaded files in the HDF5 tree viewer.

        Returns:
            A set containing the file paths of all loaded files.
        """
        return self.__loadedFiles

    def isEmpty(self) -> bool:
        """
        Check if the HDF5 tree viewer contains any loaded files.

        Returns:
            True if no files are currently loaded, False otherwise.
        """
        return len(self.__loadedFiles) == 0

    def reloadSelected(self) -> None:
        """
        Reload the currently selected HDF5 nodes.
        """
        model = self.__treeview.findHdf5TreeModel()
        for obj in self.getSelectedNodes():
            if obj.ntype is h5py.File:
                model.synchronizeH5pyObject(obj.h5py_object)

    def getSelectedNodes(self) -> list[H5Node]:
        """
        Return a list of the currently selected HDF5 nodes in the tree view.
        """
        return list(self.__treeview.selectedH5Nodes())

    def __closeAndSyncCustomContextMenu(
        self, event: silx.gui.hdf5.Hdf5ContextMenuEvent
    ) -> None:
        """
        Populate the custom context menu for the HDF5 tree viewer.

        Adds additional options to remove or reload HDF5 files in the tree view when the
        context menu is triggered.
        """
        selectedObjects = event.source().selectedH5Nodes()
        menu = event.menu()

        if not menu.isEmpty():
            menu.addSeparator()

        for obj in selectedObjects:
            if obj.ntype is h5py.File:
                action = qt.QAction("Remove %s" % obj.local_filename, event.source())
                action.triggered.connect(
                    lambda: self.__treeview.findHdf5TreeModel().removeH5pyObject(
                        obj.h5py_object
                    )
                )
                menu.addAction(action)
                action = qt.QAction("Reload %s" % obj.local_filename, event.source())
                action.triggered.connect(
                    lambda: self.__treeview.findHdf5TreeModel().synchronizeH5pyObject(
                        obj.h5py_object
                    )
                )
                menu.addAction(action)
