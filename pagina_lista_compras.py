<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <property name="sizePolicy">
    <sizepolicy hsizetype="Maximum" vsizetype="Maximum">
     <horstretch>0</horstretch>
     <verstretch>0</verstretch>
    </sizepolicy>
   </property>
   <layout class="QVBoxLayout" name="verticalLayout_2">
    <property name="spacing">
     <number>0</number>
    </property>
    <property name="leftMargin">
     <number>0</number>
    </property>
    <property name="topMargin">
     <number>0</number>
    </property>
    <property name="rightMargin">
     <number>0</number>
    </property>
    <property name="bottomMargin">
     <number>0</number>
    </property>
    <item>
     <widget class="QFrame" name="frame">
      <property name="styleSheet">
       <string notr="true">QFrame{
background-color: rgb(247, 247, 233) ;
color: rgb(176, 131, 63);
}
QPushButton{
background-color:#000000ff;
color: rgb(176, 131, 63);
border-radius:25px;
}
QPushButton:hover{
background-color:rgb(230, 225, 210);
border-radius:25px;
}</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Raised</enum>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout" stretch="1,2,1,5,1">
       <property name="spacing">
        <number>0</number>
       </property>
       <property name="leftMargin">
        <number>0</number>
       </property>
       <property name="topMargin">
        <number>0</number>
       </property>
       <property name="rightMargin">
        <number>0</number>
       </property>
       <property name="bottomMargin">
        <number>0</number>
       </property>
       <item>
        <widget class="QFrame" name="frame_2">
         <property name="frameShape">
          <enum>QFrame::StyledPanel</enum>
         </property>
         <property name="frameShadow">
          <enum>QFrame::Raised</enum>
         </property>
         <widget class="QPushButton" name="botonSalir">
          <property name="geometry">
           <rect>
            <x>740</x>
            <y>0</y>
            <width>51</width>
            <height>51</height>
           </rect>
          </property>
          <property name="minimumSize">
           <size>
            <width>40</width>
            <height>40</height>
           </size>
          </property>
          <property name="text">
           <string/>
          </property>
          <property name="icon">
           <iconset>
            <normaloff>icono-salir.png</normaloff>icono-salir.png</iconset>
          </property>
         </widget>
         <widget class="QPushButton" name="botonRegresar">
          <property name="geometry">
           <rect>
            <x>680</x>
            <y>0</y>
            <width>51</width>
            <height>51</height>
           </rect>
          </property>
          <property name="minimumSize">
           <size>
            <width>40</width>
            <height>40</height>
           </size>
          </property>
          <property name="text">
           <string/>
          </property>
          <property name="icon">
           <iconset>
            <normaloff>icono-atras.png</normaloff>icono-atras.png</iconset>
          </property>
          <property name="iconSize">
           <size>
            <width>30</width>
            <height>30</height>
           </size>
          </property>
         </widget>
        </widget>
       </item>
       <item>
        <widget class="QFrame" name="frame_3">
         <property name="font">
          <font>
           <pointsize>10</pointsize>
          </font>
         </property>
         <property name="frameShape">
          <enum>QFrame::StyledPanel</enum>
         </property>
         <property name="frameShadow">
          <enum>QFrame::Raised</enum>
         </property>
         <layout class="QHBoxLayout" name="horizontalLayout_2">
          <item>
           <widget class="QListWidget" name="listaRecetas">
            <property name="font">
             <font>
              <pointsize>10</pointsize>
             </font>
            </property>
            <property name="sizeAdjustPolicy">
             <enum>QAbstractScrollArea::AdjustToContents</enum>
            </property>
            <property name="selectionMode">
             <enum>QAbstractItemView::ExtendedSelection</enum>
            </property>
            <property name="spacing">
             <number>1</number>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QPushButton" name="botonCambiosLista">
            <property name="font">
             <font>
              <pointsize>10</pointsize>
              <weight>75</weight>
              <bold>true</bold>
             </font>
            </property>
            <property name="styleSheet">
             <string notr="true">QPushButton {
    background-color: rgb(230, 150, 150);   
    color: rgb(255, 255, 255);              
    border-radius: 20px;
    padding: 8px 16px;
    font-weight: bold;
    border: none;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.15);
}

QPushButton:hover {
    background-color: rgb(240, 130, 130);
}

QPushButton:pressed {
    background-color: rgb(220, 120, 120);
}
</string>
            </property>
            <property name="text">
             <string>Actualizar Lista</string>
            </property>
           </widget>
          </item>
         </layout>
        </widget>
       </item>
       <item>
        <widget class="QFrame" name="frame_4">
         <property name="frameShape">
          <enum>QFrame::StyledPanel</enum>
         </property>
         <property name="frameShadow">
          <enum>QFrame::Raised</enum>
         </property>
         <layout class="QHBoxLayout" name="horizontalLayout">
          <item>
           <widget class="QPushButton" name="selectTodo">
            <property name="font">
             <font>
              <pointsize>10</pointsize>
             </font>
            </property>
            <property name="styleSheet">
             <string notr="true">QFrame{
background-color: rgb(247, 247, 233) ;
}
QPushButton{
background-color:#000000ff;
border-radius:25px;
}
QPushButton:hover{
background-color:rgb(230, 225, 210);
border-radius:25px;
}</string>
            </property>
            <property name="text">
             <string>Seleccionar Todos</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QPushButton" name="borrarTodo">
            <property name="font">
             <font>
              <pointsize>10</pointsize>
             </font>
            </property>
            <property name="styleSheet">
             <string notr="true">QFrame{
background-color: rgb(247, 247, 233) ;
}
QPushButton{
background-color:#000000ff;
border-radius:25px;
}
QPushButton:hover{
background-color:rgb(230, 225, 210);
border-radius:25px;
}</string>
            </property>
            <property name="text">
             <string>Borrar Todo</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QPushButton" name="guardarLista">
            <property name="font">
             <font>
              <pointsize>10</pointsize>
             </font>
            </property>
            <property name="styleSheet">
             <string notr="true">QFrame{
background-color: rgb(247, 247, 233) ;
}
QPushButton{
background-color:#000000ff;
border-radius:25px;
}
QPushButton:hover{
background-color:rgb(230, 225, 210);
border-radius:25px;
}</string>
            </property>
            <property name="text">
             <string>Guardar Lista</string>
            </property>
           </widget>
          </item>
         </layout>
        </widget>
       </item>
       <item>
        <widget class="QFrame" name="frame_5">
         <property name="frameShape">
          <enum>QFrame::StyledPanel</enum>
         </property>
         <property name="frameShadow">
          <enum>QFrame::Raised</enum>
         </property>
         <layout class="QVBoxLayout" name="verticalLayout_3">
          <item>
           <widget class="QListWidget" name="listaCompras">
            <property name="font">
             <font>
              <pointsize>10</pointsize>
             </font>
            </property>
            <property name="sizeAdjustPolicy">
             <enum>QAbstractScrollArea::AdjustToContents</enum>
            </property>
            <property name="selectionMode">
             <enum>QAbstractItemView::ExtendedSelection</enum>
            </property>
            <property name="spacing">
             <number>1</number>
            </property>
           </widget>
          </item>
         </layout>
        </widget>
       </item>
       <item>
        <widget class="QFrame" name="frame_6">
         <property name="frameShape">
          <enum>QFrame::StyledPanel</enum>
         </property>
         <property name="frameShadow">
          <enum>QFrame::Raised</enum>
         </property>
         <widget class="QPushButton" name="botonCerrarS">
          <property name="geometry">
           <rect>
            <x>280</x>
            <y>10</y>
            <width>241</width>
            <height>41</height>
           </rect>
          </property>
          <property name="font">
           <font>
            <weight>75</weight>
            <bold>true</bold>
           </font>
          </property>
          <property name="styleSheet">
           <string notr="true"/>
          </property>
          <property name="text">
           <string>Cerrar Sesión</string>
          </property>
         </widget>
         <widget class="QPushButton" name="botonInfo">
          <property name="geometry">
           <rect>
            <x>740</x>
            <y>0</y>
            <width>51</width>
            <height>51</height>
           </rect>
          </property>
          <property name="minimumSize">
           <size>
            <width>40</width>
            <height>40</height>
           </size>
          </property>
          <property name="styleSheet">
           <string notr="true">QFrame{
background-color: rgb(247, 247, 233) ;
}
QPushButton{
background-color:#000000ff;
border-radius:25px;
}
QPushButton:hover{
background-color:rgb(230, 225, 210);
border-radius:25px;
}</string>
          </property>
          <property name="text">
           <string/>
          </property>
          <property name="icon">
           <iconset>
            <normaloff>icono-informacion.png</normaloff>icono-informacion.png</iconset>
          </property>
          <property name="iconSize">
           <size>
            <width>30</width>
            <height>30</height>
           </size>
          </property>
         </widget>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
