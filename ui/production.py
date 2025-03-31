#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de producción

Contiene la implementación de las vistas relacionadas con la producción.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QPushButton, QTableView, QFrame, QSizePolicy, QSpacerItem,
    QLineEdit, QComboBox, QHeaderView, QMessageBox, QDialog, QStyle
)
from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon

import os
from ui.production_models import ProductionTableModel, ProductionSortFilterProxyModel
from ui.icons import ADD_ICON, EDIT_ICON, DELETE_ICON, CLEAR_ICON, svg_to_icon


class ProductionControlWidget(QWidget):
    """Widget para el control de producción"""
    
    def __init__(self, parent=None):
        """
        Inicializa el widget de control de producción
        
        Args:
            parent (QWidget, optional): Widget padre
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa los componentes de la interfaz"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Título
        """ title_label = QLabel("Control de Producción")
        title_label.setObjectName("controlTitle")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(title_label) """
        
        # Descripción
        """ description_label = QLabel(
            "Esta sección le permite gestionar y monitorear el control de producción."
        )
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 11pt; margin-bottom: 20px;")
        main_layout.addWidget(description_label)
         """
        # Contenido principal
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        
        # Controles de filtrado
        filter_layout = QHBoxLayout()
        
        # Selector de tabla (oculto, pero mantenido para funcionalidad)
        self.table_selector = QComboBox()
        self.table_selector.setMinimumWidth(200)
        self.table_selector.currentIndexChanged.connect(self.load_table_data)
        self.table_selector.setVisible(False)  # Ocultar el selector
        
        # No agregamos el label ni el selector al layout
        # filter_layout.addWidget(QLabel("Tabla:"))
        # filter_layout.addWidget(self.table_selector)
        
        # filter_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))
        
        # Filtro por OF (exclusivamente)
        filter_layout.addWidget(QLabel("Filtrar por OF (Orden de Fabricación):"))
        self.of_filter = QLineEdit()
        self.of_filter.setPlaceholderText("Ingrese número de OF para filtrar...")
        self.of_filter.textChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.of_filter)
        
        # Botón para limpiar filtro con icono estándar de PySide6
        self.btn_clear_filter = QPushButton()
        self.btn_clear_filter.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.btn_clear_filter.setToolTip("Limpiar filtro")
        self.btn_clear_filter.setObjectName("btnIconClear")
        self.btn_clear_filter.clicked.connect(self.clear_filter)
        filter_layout.addWidget(self.btn_clear_filter)
        
        # Agregar espacio flexible
        filter_layout.addStretch()
        
        # Botones CRUD para la tabla
        crud_layout = QHBoxLayout()
        
        # Botón para agregar fila con icono estándar de PySide6
        self.btn_add_row = QPushButton()
        self.btn_add_row.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.btn_add_row.setToolTip("Agregar registro")
        self.btn_add_row.setObjectName("btnAddRow")
        self.btn_add_row.clicked.connect(self.show_add_row_dialog)
        crud_layout.addWidget(self.btn_add_row)
        
        # Botón para editar fila con icono estándar de PySide6
        self.btn_edit_row = QPushButton()
        self.btn_edit_row.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.btn_edit_row.setToolTip("Editar registro seleccionado")
        self.btn_edit_row.setObjectName("btnEditRow")
        self.btn_edit_row.clicked.connect(self.show_edit_row_dialog)
        crud_layout.addWidget(self.btn_edit_row)
        
        # Botón para eliminar fila con icono estándar de PySide6
        self.btn_delete_row = QPushButton()
        self.btn_delete_row.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.btn_delete_row.setToolTip("Eliminar registros seleccionados")
        self.btn_delete_row.setObjectName("btnDeleteRow")
        self.btn_delete_row.clicked.connect(self.delete_selected_rows)
        crud_layout.addWidget(self.btn_delete_row)
        
        filter_layout.addLayout(crud_layout)
        
        content_layout.addLayout(filter_layout)
        
        # Tabla de datos de producción
        self.production_table = QTableView()
        self.production_table.setObjectName("productionTable")
        self.production_table.setAlternatingRowColors(False)
        self.production_table.setSelectionBehavior(QTableView.SelectRows)
        self.production_table.setSelectionMode(QTableView.MultiSelection)  # Permitir selección múltiple
        self.production_table.setSortingEnabled(True)
        self.production_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.production_table.horizontalHeader().setStretchLastSection(True)
        
        # Ocultar los números de fila (vertical header)
        self.production_table.verticalHeader().setVisible(False)
        
        # Modelo de datos
        self.table_model = ProductionTableModel(self)
        
        # Modelo proxy para ordenamiento y filtrado
        self.proxy_model = ProductionSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.table_model)
        self.production_table.setModel(self.proxy_model)
        
        # Conectar señal de clic para manejar la selección de filas
        self.production_table.clicked.connect(self.handle_table_click)
        
        content_layout.addWidget(self.production_table)
        
        main_layout.addWidget(content_frame)
        
        # Cargar tablas disponibles
        self.load_available_tables()
    
    def load_available_tables(self):
        """Carga las tablas disponibles en la base de datos"""
        try:
            # Crear una instancia temporal para obtener las tablas
            from database.production_models import ProductionData
            import os
            
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'produccion.db')
            prod_data = ProductionData(db_path)
            
            if prod_data.connect():
                tables = prod_data.get_table_names()
                prod_data.disconnect()
                
                # Actualizar el selector de tablas
                self.table_selector.clear()
                if tables:
                    self.table_selector.addItems(tables)
                    
                    # Buscar la tabla 'bobina' y seleccionarla automáticamente
                    bobina_index = self.table_selector.findText("bobina")
                    if bobina_index >= 0:
                        self.table_selector.setCurrentIndex(bobina_index)
                    # Si no existe la tabla bobina, cargar la primera tabla disponible
                    else:
                        self.load_table_data()
                else:
                    QMessageBox.warning(
                        self, 
                        "Sin tablas", 
                        "No se encontraron tablas en la base de datos de producción."
                    )
            else:
                QMessageBox.critical(
                    self, 
                    "Error de conexión", 
                    "No se pudo conectar a la base de datos de producción."
                )
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"Error al cargar las tablas disponibles: {str(e)}"
            )
    
    def load_table_data(self, index=0):
        """Carga los datos de la tabla seleccionada"""
        if self.table_selector.count() > 0:
            table_name = self.table_selector.currentText()
            filter_text = self.of_filter.text()
            
            # Cargar datos en el modelo
            success = self.table_model.load_data(table_name, filter_text if filter_text else None)
            
            if success:
                # No es necesario ocultar la columna ID ya que no hay columna de selección
                # La columna 0 ahora es la columna OF
                pass
            else:
                QMessageBox.warning(
                    self, 
                    "Error de carga", 
                    f"No se pudieron cargar los datos de la tabla {table_name}."
                )
    
    def apply_filter(self):
        """Aplica el filtro por OF"""
        filter_text = self.of_filter.text()
        self.proxy_model.set_of_filter(filter_text)
    
    def clear_filter(self):
        """Limpia el filtro por OF"""
        self.of_filter.clear()
        self.proxy_model.set_of_filter("")
    
    def handle_table_click(self, index):
        """Maneja el clic en la tabla para la selección de filas
        
        Args:
            index (QModelIndex): Índice del modelo donde se hizo clic
        """
        # La selección ahora se maneja automáticamente por el QTableView
        # ya que está configurado con QTableView.SelectRows y QTableView.MultiSelection
        # Habilitar/deshabilitar botones según la selección
        has_selection = len(self.production_table.selectionModel().selectedRows()) > 0
        self.btn_edit_row.setEnabled(has_selection and len(self.production_table.selectionModel().selectedRows()) == 1)
        self.btn_delete_row.setEnabled(has_selection)
    
    def show_add_row_dialog(self):
        """Muestra el diálogo para agregar una nueva fila"""
        from ui.production_dialog import ProductionRecordDialog
        
        # Crear diálogo con campos apropiados para cada tipo de dato
        dialog = ProductionRecordDialog(self.table_model.column_names, None, self)
        
        # Mostrar diálogo
        if dialog.exec() == QDialog.Accepted:
            # Obtener datos del formulario
            row_data = dialog.get_row_data()
            
            # Agregar fila al modelo
            source_model = self.proxy_model.sourceModel()
            row_index = source_model.add_row(row_data)
            
            # Informar al usuario
            QMessageBox.information(
                self,
                "Registro Agregado",
                "El registro ha sido agregado correctamente a la tabla. \nNota: Los cambios solo se mantienen en memoria y no se guardan en la base de datos."
            )
    
    def show_edit_row_dialog(self):
        """Muestra el diálogo para editar una fila seleccionada"""
        # Obtener la fila seleccionada
        selected_rows = self.production_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(
                self,
                "Sin Selección",
                "Por favor, seleccione un registro para editar."
            )
            return
        
        # Solo permitir editar una fila a la vez
        if len(selected_rows) > 1:
            QMessageBox.warning(
                self,
                "Múltiples Selecciones",
                "Por favor, seleccione solo un registro para editar."
            )
            return
        
        # Obtener el índice de la fila seleccionada en el modelo proxy
        proxy_index = selected_rows[0]
        # Convertir al índice en el modelo fuente
        source_index = self.proxy_model.mapToSource(proxy_index)
        row_index = source_index.row()
        
        # Obtener los datos actuales de la fila
        current_row_data = self.table_model.data_rows[row_index]
        
        # Crear diálogo con campos apropiados para cada tipo de dato
        from ui.production_dialog import ProductionRecordDialog
        dialog = ProductionRecordDialog(self.table_model.column_names, current_row_data, self)
        
        # Mostrar diálogo
        if dialog.exec() == QDialog.Accepted:
            # Obtener datos del formulario
            row_data = dialog.get_row_data()
            
            # Actualizar fila en el modelo
            self.table_model.update_row(row_index, row_data)
            
            # Informar al usuario
            QMessageBox.information(
                self,
                "Registro Actualizado",
                "El registro ha sido actualizado correctamente en la tabla. \nNota: Los cambios solo se mantienen en memoria y no se guardan en la base de datos."
            )
    
    def delete_selected_rows(self):
        """Elimina las filas seleccionadas"""
        # Obtener las filas seleccionadas
        selected_rows = self.production_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(
                self,
                "Sin Selección",
                "Por favor, seleccione al menos un registro para eliminar."
            )
            return
        
        # Confirmar eliminación
        confirm = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar {len(selected_rows)} registro(s)?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Convertir índices del modelo proxy al modelo fuente y ordenarlos en orden descendente
            # para evitar problemas al eliminar múltiples filas
            source_indices = [self.proxy_model.mapToSource(index).row() for index in selected_rows]
            source_indices.sort(reverse=True)
            
            # Eliminar filas
            for row_index in source_indices:
                self.table_model.delete_row(row_index)
            
            # Informar al usuario
            QMessageBox.information(
                self,
                "Registros Eliminados",
                f"{len(selected_rows)} registro(s) han sido eliminados correctamente de la tabla. \nNota: Los cambios solo se mantienen en memoria y no se guardan en la base de datos."
            )
            
            # Deshabilitar botones de edición y eliminación
            self.btn_edit_row.setEnabled(False)
            self.btn_delete_row.setEnabled(False)


class ProductionOFControlWidget(QWidget):
    """Widget para el control de órdenes de fabricación"""
    
    def __init__(self, parent=None):
        """
        Inicializa el widget de control de órdenes de fabricación
        
        Args:
            parent (QWidget, optional): Widget padre
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa los componentes de la interfaz"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Título
        """ title_label = QLabel("Control de Órdenes de Fabricación")
        title_label.setObjectName("ofControlTitle")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
         """
        # Descripción
        """ description_label = QLabel(
            "Esta sección le permite gestionar y monitorear las órdenes de fabricación."
        )
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 11pt; margin-bottom: 20px;")
        main_layout.addWidget(description_label) """
        
        # Contenido principal (a implementar según requerimientos específicos)
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        
        # Placeholder para contenido futuro
        placeholder_label = QLabel("Contenido del Control de Órdenes de Fabricación (a implementar)")
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_label.setStyleSheet("font-size: 14pt; color: gray;")
        content_layout.addWidget(placeholder_label)
        
        main_layout.addWidget(content_frame)
        
        # Espaciador para empujar todo hacia arriba
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))