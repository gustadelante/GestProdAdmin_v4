
"""

"""

)
import json
import os


class ProductionRecordDialog(QDialog):
    
        """
        
        Args:
            parent (QWidget, optional): Widget padre
        """
        
            "Productos": [],
            "Alistamiento": [],
            "Calidad": [],
            "Observaciones": []
        }
        try:
                data = json.load(f)
        except Exception as e:
        
        
        
    
        """
        
        Args:
        """
        
        )
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content)
        
        form_layout = QFormLayout()
        
        
        
                widget = QComboBox()
                widget.setEditable(False)
                    widget.addItem(f"{item['codigo']} - {item['nombre']}", item['codigo'])
                widget = QComboBox()
                widget.setEditable(False)
                    widget.addItem(f"{item['codigo']} - {item['nombre']}", item['codigo'])
                widget = QComboBox()
                widget.setEditable(False)
                    widget.addItem(f"{item['codigo']} - {item['nombre']}", item['codigo'])
                widget = QComboBox()
                widget.setEditable(False)
                    widget.addItem(f"{item['codigo']} - {item['nombre']}", item['codigo'])
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                widget.setDate(QDate.currentDate())
                    try:
                        date_parts = row_data[col_idx].split("-")
                    except:
                        pass
                widget.setRange(0, 9999.99)
                widget.setDecimals(2)
                    try:
                        widget.setValue(float(row_data[col_idx]))
                    except:
                        pass
                widget = QComboBox()
                widget.setEditable(False)
                widget.addItems(["A", "B", "C", "D"])
                widget.setRange(0, 999999)
                    try:
                    except:
                        pass
            
            form_layout.addRow(f"{col_name}:", widget)
        
        
        scroll_content_layout.addLayout(form_layout)
        
        scroll_area.setWidget(scroll_content)
        
        layout.addWidget(button_box)
    
        """
        """
                "Validaci??n",
            )
            return
        
    
        """
        
        Returns:
        """
        row_data = []
        
            
                value = widget.currentData()
                value = nombre.upper()
                value = str(widget.value())
                value = str(widget.value())
                text = widget.currentText()
                    value = text.split(" - ")[0].strip()
                    value = text
                value = widget.text()
            
            row_data.append(value)
        
        return row_data
