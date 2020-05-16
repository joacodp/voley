import docplex
cantidad_de_fechas_ampliada = 27
cantidad_de_fechas = 18
cantidad_de_dias = 130
#sol = ['partido_6_9_7', 'partido_3_0_24', 'partido_5_1_15', 'partido_7_4_20', 'partido_9_3_5', 'partido_0_7_6', 'partido_3_1_4', 'partido_2_3_13', 'partido_7_2_4', 'partido_7_8_8', 'partido_8_4_19', 'partido_4_6_4', 'partido_9_8_2', 'partido_8_3_20', 'partido_5_0_0', 'partido_9_2_17', 'partido_0_9_14', 'partido_0_3_19', 'partido_6_1_6', 'partido_8_1_13', 'partido_4_5_13', 'partido_1_8_23', 'partido_8_0_5', 'partido_2_5_23', 'partido_5_6_9', 'partido_9_7_24', 'partido_2_4_9', 'partido_1_4_2', 'partido_7_5_5', 'partido_2_6_20', 'partido_6_4_8', 'partido_7_6_13', 'partido_2_0_26', 'partido_9_1_20', 'partido_8_2_3', 'partido_3_4_10', 'partido_0_4_18', 'partido_5_4_14', 'partido_1_9_1', 'partido_2_8_18', 'partido_7_9_16', 'partido_0_6_15', 'partido_5_8_26', 'partido_9_0_23', 'partido_6_5_24', 'partido_1_7_0', 'partido_1_2_10', 'partido_8_9_15', 'partido_4_2_16', 'partido_1_0_16', 'partido_9_5_12', 'partido_3_5_11', 'partido_1_3_7', 'partido_7_3_21', 'partido_4_8_1', 'partido_5_2_25', 'partido_0_8_11', 'partido_7_0_10', 'partido_9_6_3', 'partido_2_1_5', 'partido_6_2_21', 'partido_9_4_26', 'partido_3_6_2', 'partido_0_2_2', 'partido_4_3_6', 'partido_6_0_25', 'partido_3_9_9', 'partido_3_8_0', 'partido_6_7_18', 'partido_2_7_19', 'partido_3_7_26', 'partido_1_5_17', 'partido_4_9_11', 'partido_7_1_14', 'partido_5_9_21', 'partido_8_5_6', 'partido_3_2_15', 'partido_4_7_25', 'partido_6_3_12', 'partido_4_0_22', 'partido_5_7_2', 'partido_0_1_12', 'partido_6_8_17', 'partido_0_5_7', 'partido_5_3_18', 'partido_4_1_21', 'partido_1_6_26', 'partido_2_9_8', 'partido_8_7_12', 'partido_8_6_14', 'viaje_25_0_6_2_preferido', 'viaje_22_0_4_9_3_preferido', 'viaje_16_0_1_preferido', 'viaje_0_0_5_preferido', 'viaje_10_0_7_preferido', 'viaje_5_0_8_preferido', 'viaje_12_1_0_8_7_5_preferido', 'viaje_4_1_3_2_6_preferido', 'viaje_20_1_9_4_preferido', 'viaje_2_2_0_8_7_preferido', 'viaje_15_2_3_4_9_preferido', 'viaje_10_2_1_preferido', 'viaje_25_2_5_preferido', 'viaje_21_2_6_preferido', 'viaje_18_3_5_0_8_7_preferido', 'viaje_12_3_6_2_preferido', 'viaje_5_3_9_4_1_preferido', 'viaje_18_4_0_8_7_preferido', 'viaje_8_4_6_2_3_preferido', 'viaje_2_4_1_preferido', 'viaje_14_4_5_preferido', 'viaje_26_4_9_preferido', 'viaje_5_5_7_8_0_preferido', 'viaje_23_5_2_6_preferido', 'viaje_11_5_3_9_4_preferido', 'viaje_17_5_1_preferido', 'viaje_13_6_7_8_0_preferido', 'viaje_2_6_3_9_4_preferido', 'viaje_26_6_1_preferido', 'viaje_20_6_2_preferido', 'viaje_9_6_5_preferido', 'viaje_18_7_6_2_preferido', 'viaje_24_7_9_4_3_preferido', 'viaje_6_7_0_preferido', 'viaje_0_7_1_preferido', 'viaje_2_7_5_preferido', 'viaje_12_7_8_preferido', 'viaje_17_8_6_2_preferido', 'viaje_0_8_3_4_9_preferido', 'viaje_11_8_0_preferido', 'viaje_23_8_1_preferido', 'viaje_26_8_5_preferido', 'viaje_8_8_7_preferido', 'viaje_14_9_0_8_7_preferido', 'viaje_7_9_6_2_3_preferido', 'viaje_1_9_1_preferido', 'viaje_11_9_4_preferido', 'viaje_21_9_5_preferido']
#la buena ->
#sol = ['partido_9_0_24', 'partido_5_6_13', 'partido_4_1_22', 'partido_5_0_14', 'partido_0_1_5', 'partido_6_4_7', 'partido_2_8_16', 'partido_8_3_14', 'partido_1_9_1', 'partido_4_5_16', 'partido_8_5_22', 'partido_7_0_8', 'partido_0_6_2', 'partido_1_0_3', 'partido_6_5_5', 'partido_1_6_19', 'partido_9_6_26', 'partido_2_9_20', 'partido_9_3_6', 'partido_1_5_11', 'partido_7_9_13', 'partido_0_5_21', 'partido_3_7_2', 'partido_9_2_25', 'partido_3_5_18', 'partido_2_5_4', 'partido_4_2_24', 'partido_3_1_16', 'partido_5_2_1', 'partido_8_2_13', 'partido_4_9_15', 'partido_9_4_4', 'partido_2_4_8', 'partido_9_8_9', 'partido_4_7_1', 'partido_8_6_3', 'partido_5_4_26', 'partido_6_1_14', 'partido_2_7_10', 'partido_3_9_19', 'partido_0_3_13', 'partido_3_8_8', 'partido_6_9_21', 'partido_7_4_18', 'partido_7_5_23', 'partido_8_4_19', 'partido_6_3_22', 'partido_4_3_5', 'partido_2_3_21', 'partido_1_4_12', 'partido_0_9_11', 'partido_5_8_2', 'partido_3_0_25', 'partido_5_3_12', 'partido_6_7_11', 'partido_7_6_4', 'partido_7_2_14', 'partido_4_0_23', 'partido_7_1_7', 'partido_4_8_10', 'partido_0_4_20', 'partido_8_7_5', 'partido_0_7_16', 'partido_7_8_24', 'partido_8_0_7', 'partido_6_2_6', 'partido_4_6_25', 'partido_5_7_20', 'partido_7_3_15', 'partido_2_1_15', 'partido_8_9_12', 'partido_0_2_12', 'partido_1_7_26', 'partido_3_4_9', 'partido_8_1_6', 'partido_1_2_18', 'partido_1_8_20', 'partido_5_9_7', 'partido_9_7_0', 'partido_0_8_26', 'partido_9_5_17', 'partido_3_2_26', 'partido_2_6_9', 'partido_1_3_4', 'partido_9_1_23', 'partido_6_0_18', 'partido_3_6_24', 'partido_5_1_8', 'partido_6_8_17', 'partido_2_0_19', 'viaje_18_0_6_2_preferido', 'viaje_23_0_4_9_3_preferido', 'viaje_3_0_1_preferido', 'viaje_14_0_5_preferido', 'viaje_8_0_7_preferido', 'viaje_7_0_8_preferido', 'viaje_5_1_0_8_7_5_preferido', 'viaje_14_1_6_2_3_preferido', 'viaje_22_1_4_9_preferido', 'viaje_12_2_0_8_7_preferido', 'viaje_24_2_4_9_3_preferido', 'viaje_18_2_1_preferido', 'viaje_1_2_5_preferido', 'viaje_6_2_6_preferido', 'viaje_12_3_5_0_8_7_preferido', 'viaje_21_3_2_6_preferido', 'viaje_4_3_1_4_9_preferido', 'viaje_18_4_7_8_0_preferido', 'viaje_7_4_6_2_3_preferido', 'viaje_12_4_1_preferido', 'viaje_26_4_5_preferido', 'viaje_4_4_9_preferido', 'viaje_21_5_0_8_7_preferido', 'viaje_4_5_2_6_preferido', 'viaje_16_5_4_9_3_preferido', 'viaje_11_5_1_preferido', 'viaje_2_6_0_8_7_preferido', 'viaje_24_6_3_4_9_preferido', 'viaje_19_6_1_preferido', 'viaje_9_6_2_preferido', 'viaje_13_6_5_preferido', 'viaje_10_7_2_6_preferido', 'viaje_0_7_9_4_3_preferido', 'viaje_16_7_0_preferido', 'viaje_26_7_1_preferido', 'viaje_20_7_5_preferido', 'viaje_5_7_8_preferido', 'viaje_16_8_2_6_preferido', 'viaje_8_8_3_9_4_preferido', 'viaje_26_8_0_preferido', 'viaje_20_8_1_preferido', 'viaje_2_8_5_preferido', 'viaje_24_8_7_preferido', 'viaje_11_9_0_8_7_preferido', 'viaje_19_9_3_2_6_preferido', 'viaje_1_9_1_preferido', 'viaje_15_9_4_preferido', 'viaje_7_9_5_preferido']
#la nueva ->
#sol = ['partido_7_6_15', 'partido_8_4_12', 'partido_4_5_1', 'partido_7_0_26', 'partido_9_5_2', 'partido_2_9_16', 'partido_9_8_3', 'partido_6_4_6', 'partido_8_6_14', 'partido_5_7_12', 'partido_5_8_26', 'partido_0_8_22', 'partido_9_2_11', 'partido_6_5_16', 'partido_2_5_15', 'partido_4_3_21', 'partido_1_5_9', 'partido_4_1_15', 'partido_1_9_13', 'partido_0_4_14', 'partido_2_8_17', 'partido_2_0_1', 'partido_0_3_12', 'partido_2_7_8', 'partido_0_9_9', 'partido_1_7_2', 'partido_0_1_8', 'partido_7_4_13', 'partido_9_7_18', 'partido_7_5_22', 'partido_1_8_11', 'partido_9_0_6', 'partido_1_2_3', 'partido_1_6_20', 'partido_2_6_2', 'partido_7_9_7', 'partido_8_2_20', 'partido_9_1_14', 'partido_5_3_11', 'partido_3_7_16', 'partido_8_9_8', 'partido_0_2_19', 'partido_1_0_10', 'partido_2_4_7', 'partido_2_1_22', 'partido_8_0_16', 'partido_4_9_22', 'partido_8_3_13', 'partido_1_3_19', 'partido_8_5_23', 'partido_8_1_7', 'partido_4_0_5', 'partido_3_4_8', 'partido_6_8_18', 'partido_5_1_5', 'partido_6_7_9', 'partido_4_2_10', 'partido_9_3_20', 'partido_3_8_1', 'partido_3_9_26', 'partido_5_2_14', 'partido_0_5_24', 'partido_4_8_2', 'partido_4_7_17', 'partido_3_0_4', 'partido_3_6_22', 'partido_1_4_26', 'partido_7_1_6', 'partido_6_1_21', 'partido_6_3_5', 'partido_5_9_4', 'partido_6_2_26', 'partido_0_7_3', 'partido_3_5_3', 'partido_5_6_8', 'partido_4_6_23', 'partido_2_3_6', 'partido_5_0_21', 'partido_0_6_13', 'partido_5_4_20', 'partido_3_2_9', 'partido_6_9_17', 'partido_9_4_0', 'partido_7_3_14', 'partido_9_6_24', 'partido_7_8_5', 'partido_8_7_24', 'partido_6_0_0', 'partido_3_1_23', 'partido_7_2_21', 'viaje_0_0_6_2_preferido', 'viaje_4_0_3_4_9_preferido', 'viaje_10_0_1_preferido', 'viaje_21_0_5_preferido', 'viaje_26_0_7_preferido', 'viaje_16_0_8_preferido', 'viaje_5_1_5_7_8_0_preferido', 'viaje_21_1_6_2_3_preferido', 'viaje_14_1_9_4_preferido', 'viaje_19_2_0_8_7_preferido', 'viaje_9_2_3_4_9_preferido', 'viaje_3_2_1_preferido', 'viaje_14_2_5_preferido', 'viaje_26_2_6_preferido', 'viaje_11_3_5_0_8_7_preferido', 'viaje_5_3_6_2_preferido', 'viaje_19_3_1_9_4_preferido', 'viaje_12_4_8_7_0_preferido', 'viaje_6_4_6_2_3_preferido', 'viaje_26_4_1_preferido', 'viaje_20_4_5_preferido', 'viaje_0_4_9_preferido', 'viaje_22_5_7_8_0_preferido', 'viaje_15_5_2_6_preferido', 'viaje_1_5_4_9_3_preferido', 'viaje_9_5_1_preferido', 'viaje_13_6_0_8_7_preferido', 'viaje_22_6_3_4_9_preferido', 'viaje_20_6_1_preferido', 'viaje_2_6_2_preferido', 'viaje_8_6_5_preferido', 'viaje_8_7_2_6_preferido', 'viaje_16_7_3_4_9_preferido', 'viaje_3_7_0_preferido', 'viaje_2_7_1_preferido', 'viaje_12_7_5_preferido', 'viaje_24_7_8_preferido', 'viaje_17_8_2_6_preferido', 'viaje_1_8_3_4_9_preferido', 'viaje_22_8_0_preferido', 'viaje_11_8_1_preferido', 'viaje_26_8_5_preferido', 'viaje_5_8_7_preferido', 'viaje_7_9_7_8_0_preferido', 'viaje_16_9_2_6_preferido', 'viaje_13_9_1_preferido', 'viaje_26_9_3_preferido', 'viaje_22_9_4_preferido', 'viaje_4_9_5_preferido']
sol = ['partido_6_8_13', 'partido_2_0_25', 'partido_5_1_19', 'partido_7_1_20', 'partido_6_7_23', 'partido_6_5_18', 'partido_5_8_7', 'partido_4_6_14', 'partido_7_9_21', 'partido_3_5_3', 'partido_6_0_24', 'partido_0_7_26', 'partido_6_3_5', 'partido_2_8_14', 'partido_5_0_14', 'partido_0_4_10', 'partido_0_9_19', 'partido_3_0_8', 'partido_8_2_1', 'partido_0_2_2', 'partido_2_4_3', 'partido_6_9_10', 'partido_2_5_17', 'partido_7_3_18', 'partido_7_2_0', 'partido_6_4_4', 'partido_0_1_22', 'partido_0_5_11', 'partido_4_0_7', 'partido_8_9_20', 'partido_1_5_24', 'partido_8_5_10', 'partido_5_3_21', 'partido_8_0_18', 'partido_0_6_9', 'partido_9_8_23', 'partido_1_9_3', 'partido_2_9_9', 'partido_8_4_11', 'partido_4_5_5', 'partido_9_5_4', 'partido_4_2_21', 'partido_1_6_1', 'partido_1_0_0', 'partido_2_3_6', 'partido_5_6_20', 'partido_3_7_15', 'partido_3_6_16', 'partido_8_1_21', 'partido_2_1_13', 'partido_3_4_2', 'partido_9_6_15', 'partido_3_2_23', 'partido_4_9_0', 'partido_5_7_1', 'partido_7_5_9', 'partido_0_8_16', 'partido_4_1_6', 'partido_3_8_24', 'partido_0_3_20', 'partido_2_6_26', 'partido_8_3_19', 'partido_4_3_13', 'partido_7_4_12', 'partido_1_2_8', 'partido_8_6_8', 'partido_1_3_11', 'partido_9_7_16', 'partido_9_1_5', 'partido_7_0_13', 'partido_4_7_17', 'partido_2_7_24', 'partido_5_9_13', 'partido_5_4_26', 'partido_8_7_4', 'partido_4_8_22', 'partido_9_3_12', 'partido_6_1_12', 'partido_7_6_7', 'partido_3_1_14', 'partido_3_9_26', 'partido_1_4_18', 'partido_9_2_22', 'partido_9_4_24', 'partido_7_8_3', 'partido_9_0_6', 'partido_6_2_11', 'partido_5_2_15', 'partido_1_7_10', 'partido_1_8_26', 'viaje_24_0_6_2_preferido', 'viaje_6_0_9_4_3_preferido', 'viaje_0_0_1_preferido', 'viaje_14_0_5_preferido', 'viaje_13_0_7_preferido', 'viaje_18_0_8_preferido', 'viaje_19_1_5_7_8_0_preferido', 'viaje_12_1_6_2_3_preferido', 'viaje_5_1_9_4_preferido', 'viaje_0_2_7_8_0_preferido', 'viaje_21_2_4_9_3_preferido', 'viaje_8_2_1_preferido', 'viaje_15_2_5_preferido', 'viaje_11_2_6_preferido', 'viaje_18_3_7_8_0_5_preferido', 'viaje_5_3_6_2_preferido', 'viaje_11_3_1_9_4_preferido', 'viaje_10_4_0_8_7_preferido', 'viaje_2_4_3_2_6_preferido', 'viaje_18_4_1_preferido', 'viaje_26_4_5_preferido', 'viaje_24_4_9_preferido', 'viaje_9_5_7_8_0_preferido', 'viaje_17_5_2_6_preferido', 'viaje_3_5_3_9_4_preferido', 'viaje_24_5_1_preferido', 'viaje_7_6_7_8_0_preferido', 'viaje_14_6_4_9_3_preferido', 'viaje_1_6_1_preferido', 'viaje_26_6_2_preferido', 'viaje_20_6_5_preferido', 'viaje_23_7_6_2_preferido', 'viaje_15_7_3_9_4_preferido', 'viaje_26_7_0_preferido', 'viaje_10_7_1_preferido', 'viaje_1_7_5_preferido', 'viaje_4_7_8_preferido', 'viaje_13_8_6_2_preferido', 'viaje_22_8_4_9_3_preferido', 'viaje_16_8_0_preferido', 'viaje_26_8_1_preferido', 'viaje_7_8_5_preferido', 'viaje_3_8_7_preferido', 'viaje_19_9_0_8_7_preferido', 'viaje_9_9_2_6_preferido', 'viaje_3_9_1_preferido', 'viaje_26_9_3_preferido', 'viaje_0_9_4_preferido', 'viaje_13_9_5_preferido']
#sol = ['partido_8_2_13', 'partido_7_4_21', 'partido_7_2_12', 'partido_5_2_24', 'partido_3_7_18', 'partido_4_6_1', 'partido_1_7_8', 'partido_2_7_26', 'partido_0_2_14', 'partido_8_4_20', 'partido_1_9_15', 'partido_8_7_11', 'partido_9_4_4', 'partido_2_1_20', 'partido_6_3_23', 'partido_6_5_4', 'partido_7_6_15', 'partido_5_1_3', 'partido_5_7_2', 'partido_6_1_19', 'partido_6_4_24', 'partido_6_2_8', 'partido_2_3_22', 'partido_0_4_19', 'partido_7_8_1', 'partido_4_8_8', 'partido_1_3_14', 'partido_9_2_18', 'partido_2_0_9', 'partido_5_0_25', 'partido_5_4_14', 'partido_4_9_5', 'partido_1_0_16', 'partido_1_6_26', 'partido_1_4_9', 'partido_9_3_16', 'partido_3_5_20', 'partido_1_8_23', 'partido_3_1_21', 'partido_2_9_10', 'partido_9_6_0', 'partido_0_7_20', 'partido_8_9_25', 'partido_2_5_5', 'partido_6_0_10', 'partido_4_7_16', 'partido_0_6_13', 'partido_3_2_19', 'partido_3_9_11', 'partido_5_8_26', 'partido_5_3_8', 'partido_4_2_17', 'partido_7_5_13', 'partido_2_8_15', 'partido_3_8_9', 'partido_7_1_4', 'partido_0_9_26', 'partido_8_3_6', 'partido_6_7_25', 'partido_0_8_18', 'partido_5_6_7', 'partido_8_1_5', 'partido_2_6_21', 'partido_8_0_4', 'partido_6_8_16', 'partido_4_1_12', 'partido_9_1_13', 'partido_1_2_2', 'partido_5_9_19', 'partido_8_6_14', 'partido_3_6_2', 'partido_9_0_3', 'partido_8_5_12', 'partido_0_3_7', 'partido_9_5_21', 'partido_9_7_17', 'partido_1_5_17', 'partido_2_4_25', 'partido_4_0_2', 'partido_4_5_22', 'partido_7_0_22', 'partido_7_3_5', 'partido_0_1_6', 'partido_9_8_7', 'partido_3_0_1', 'partido_4_3_15', 'partido_7_9_24', 'partido_6_9_9', 'partido_3_4_26', 'partido_0_5_11', 'viaje_9_0_2_6_preferido', 'viaje_1_0_3_4_9_preferido', 'viaje_16_0_1_preferido', 'viaje_25_0_5_preferido', 'viaje_22_0_7_preferido', 'viaje_4_0_8_preferido', 'viaje_3_1_5_7_8_0_preferido', 'viaje_19_1_6_2_3_preferido', 'viaje_12_1_4_9_preferido', 'viaje_12_2_7_8_0_preferido', 'viaje_17_2_4_9_3_preferido', 'viaje_2_2_1_preferido', 'viaje_24_2_5_preferido', 'viaje_8_2_6_preferido', 'viaje_5_3_7_8_0_5_preferido', 'viaje_22_3_2_6_preferido', 'viaje_14_3_1_4_9_preferido', 'viaje_19_4_0_8_7_preferido', 'viaje_24_4_6_2_3_preferido', 'viaje_9_4_1_preferido', 'viaje_14_4_5_preferido', 'viaje_4_4_9_preferido', 'viaje_11_5_0_8_7_preferido', 'viaje_4_5_6_2_preferido', 'viaje_20_5_3_9_4_preferido', 'viaje_17_5_1_preferido', 'viaje_13_6_0_8_7_preferido', 'viaje_0_6_9_4_3_preferido', 'viaje_26_6_1_preferido', 'viaje_21_6_2_preferido', 'viaje_7_6_5_preferido', 'viaje_25_7_6_2_preferido', 'viaje_16_7_4_9_3_preferido', 'viaje_20_7_0_preferido', 'viaje_8_7_1_preferido', 'viaje_2_7_5_preferido', 'viaje_11_7_8_preferido', 'viaje_15_8_2_6_preferido', 'viaje_7_8_9_4_3_preferido', 'viaje_18_8_0_preferido', 'viaje_23_8_1_preferido', 'viaje_26_8_5_preferido', 'viaje_1_8_7_preferido', 'viaje_24_9_7_8_0_preferido', 'viaje_9_9_6_2_3_preferido', 'viaje_15_9_1_preferido', 'viaje_5_9_4_preferido', 'viaje_19_9_5_preferido']
#sol = ['partido_0_1_11', 'partido_0_2_5', 'partido_0_3_6', 'partido_0_4_19', 'partido_0_5_22', 'partido_0_6_9', 'partido_0_7_16', 'partido_0_8_20', 'partido_0_9_10', 'partido_1_0_7', 'partido_1_2_24', 'partido_1_3_19', 'partido_1_4_1', 'partido_1_5_9', 'partido_1_6_17', 'partido_1_7_2', 'partido_1_8_8', 'partido_1_9_26', 'partido_2_0_26', 'partido_2_1_21', 'partido_2_3_14', 'partido_2_4_25', 'partido_2_5_15', 'partido_2_6_22', 'partido_2_7_6', 'partido_2_8_1', 'partido_2_9_18', 'partido_3_0_1', 'partido_3_1_22', 'partido_3_2_10', 'partido_3_4_26', 'partido_3_5_3', 'partido_3_6_4', 'partido_3_7_24', 'partido_3_8_13', 'partido_3_9_17', 'partido_4_0_3', 'partido_4_1_5', 'partido_4_2_9', 'partido_4_3_21', 'partido_4_5_2', 'partido_4_6_6', 'partido_4_7_23', 'partido_4_8_15', 'partido_4_9_4', 'partido_5_0_13', 'partido_5_1_14', 'partido_5_2_19', 'partido_5_3_5', 'partido_5_4_12', 'partido_5_6_26', 'partido_5_7_10', 'partido_5_8_6', 'partido_5_9_24', 'partido_6_0_25', 'partido_6_1_20', 'partido_6_2_13', 'partido_6_3_15', 'partido_6_4_24', 'partido_6_5_16', 'partido_6_7_7', 'partido_6_8_2', 'partido_6_9_19', 'partido_7_0_18', 'partido_7_1_13', 'partido_7_2_3', 'partido_7_3_8', 'partido_7_4_17', 'partido_7_5_20', 'partido_7_6_11', 'partido_7_8_26', 'partido_7_9_12', 'partido_8_0_24', 'partido_8_1_12', 'partido_8_2_4', 'partido_8_3_7', 'partido_8_4_18', 'partido_8_5_21', 'partido_8_6_10', 'partido_8_7_0', 'partido_8_9_11', 'partido_9_0_2', 'partido_9_1_6', 'partido_9_2_8', 'partido_9_3_20', 'partido_9_4_7', 'partido_9_5_1', 'partido_9_6_5', 'partido_9_7_22', 'partido_9_8_14', 'viaje_25_0_6_2_preferido', 'viaje_1_0_3_9_4_preferido', 'viaje_7_0_1_preferido', 'viaje_13_0_5_preferido', 'viaje_18_0_7_preferido', 'viaje_24_0_8_preferido', 'viaje_11_1_0_8_7_5_preferido', 'viaje_20_1_6_2_3_preferido', 'viaje_5_1_4_9_preferido', 'viaje_3_2_7_8_0_preferido', 'viaje_8_2_9_4_3_preferido', 'viaje_24_2_1_preferido', 'viaje_19_2_5_preferido', 'viaje_13_2_6_preferido', 'viaje_5_3_5_0_8_7_preferido', 'viaje_14_3_2_6_preferido', 'viaje_19_3_1_9_4_preferido', 'viaje_17_4_7_8_0_preferido', 'viaje_24_4_6_2_3_preferido', 'viaje_1_4_1_preferido', 'viaje_12_4_5_preferido', 'viaje_7_4_9_preferido', 'viaje_20_5_7_8_0_preferido', 'viaje_15_5_2_6_preferido', 'viaje_1_5_9_4_3_preferido', 'viaje_9_5_1_preferido', 'viaje_9_6_0_8_7_preferido', 'viaje_4_6_3_9_4_preferido', 'viaje_17_6_1_preferido', 'viaje_22_6_2_preferido', 'viaje_26_6_5_preferido', 'viaje_6_7_2_6_preferido', 'viaje_22_7_9_4_3_preferido', 'viaje_16_7_0_preferido', 'viaje_2_7_1_preferido', 'viaje_10_7_5_preferido', 'viaje_0_7_8_preferido', 'viaje_1_8_2_6_preferido', 'viaje_13_8_3_9_4_preferido', 'viaje_20_8_0_preferido', 'viaje_8_8_1_preferido', 'viaje_6_8_5_preferido', 'viaje_26_8_7_preferido', 'viaje_10_9_0_8_7_preferido', 'viaje_17_9_3_2_6_preferido', 'viaje_26_9_1_preferido', 'viaje_4_9_4_preferido', 'viaje_24_9_5_preferido']
#erroneosol = ['partido_2_5_1', 'partido_0_6_19', 'partido_0_2_20', 'partido_6_2_16', 'partido_0_7_26', 'partido_4_7_17', 'partido_5_9_19', 'partido_8_2_21', 'partido_7_1_20', 'partido_4_8_25', 'partido_2_4_2', 'partido_7_5_8', 'partido_4_2_9', 'partido_7_6_21', 'partido_5_4_12', 'partido_5_6_11', 'partido_3_9_4', 'partido_4_3_20', 'partido_1_6_15', 'partido_4_9_13', 'partido_9_5_14', 'partido_2_0_24', 'partido_0_5_7', 'partido_6_3_5', 'partido_4_1_7', 'partido_5_0_13', 'partido_8_9_2', 'partido_9_3_21', 'partido_4_0_10', 'partido_9_2_8', 'partido_8_0_3', 'partido_1_7_5', 'partido_2_9_25', 'partido_2_1_14', 'partido_3_7_18', 'partido_1_3_2', 'partido_1_5_22', 'partido_6_0_23', 'partido_2_7_11', 'partido_5_8_26', 'partido_8_4_5', 'partido_8_6_20', 'partido_9_6_7', 'partido_3_6_9', 'partido_6_1_13', 'partido_8_3_13', 'partido_8_7_14', 'partido_6_7_10', 'partido_7_0_15', 'partido_9_7_16', 'partido_3_0_11', 'partido_7_9_3', 'partido_3_2_10', 'partido_2_6_3', 'partido_8_5_9', 'partido_1_0_17', 'partido_6_4_1', 'partido_7_2_22', 'partido_0_8_6', 'partido_0_9_1', 'partido_0_3_14', 'partido_1_4_23', 'partido_6_8_17', 'partido_1_9_10', 'partido_4_5_15', 'partido_3_1_8', 'partido_1_2_26', 'partido_0_1_21', 'partido_3_8_23', 'partido_7_3_12', 'partido_2_3_6', 'partido_1_8_11', 'partido_7_8_1', 'partido_3_5_16', 'partido_5_1_4', 'partido_3_4_26', 'partido_9_8_24', 'partido_9_1_6', 'partido_8_1_19', 'partido_4_6_8', 'partido_9_0_9', 'partido_7_4_6', 'partido_6_9_26', 'partido_0_4_4', 'partido_6_5_2', 'partido_5_7_23', 'partido_5_2_5', 'partido_5_3_3', 'partido_2_8_18', 'partido_9_4_18', 'viaje_23_0_6_2_preferido', 'viaje_9_0_9_4_3_preferido', 'viaje_17_0_1_preferido', 'viaje_13_0_5_preferido', 'viaje_15_0_7_preferido', 'viaje_3_0_8_preferido', 'viaje_19_1_8_7_0_preferido', 'viaje_13_1_6_2_preferido', 'viaje_6_1_9_4_3_preferido', 'viaje_4_1_5_preferido', 'viaje_20_2_0_8_7_preferido', 'viaje_8_2_9_4_3_preferido', 'viaje_26_2_1_preferido', 'viaje_5_2_5_preferido', 'viaje_16_2_6_preferido', 'viaje_12_3_7_8_0_preferido', 'viaje_5_3_6_2_preferido', 'viaje_20_3_4_9_preferido', 'viaje_4_4_0_8_7_preferido', 'viaje_1_4_6_2_4_preferido', 'viaje_23_4_1_preferido', 'viaje_26_4_3_preferido', 'viaje_12_4_5_preferido', 'viaje_18_4_9_preferido', 'viaje_7_5_0_7_8_preferido', 'viaje_1_5_2_6_preferido', 'viaje_14_5_9_4_3_preferido', 'viaje_22_5_1_preferido', 'viaje_19_6_0_8_7_preferido', 'viaje_7_6_9_4_3_preferido', 'viaje_15_6_1_preferido', 'viaje_3_6_2_preferido', 'viaje_11_6_5_preferido', 'viaje_10_7_6_2_preferido', 'viaje_16_7_9_4_3_preferido', 'viaje_26_7_0_preferido', 'viaje_5_7_1_preferido', 'viaje_23_7_5_preferido', 'viaje_14_7_8_preferido', 'viaje_17_8_6_2_preferido', 'viaje_23_8_3_9_4_preferido', 'viaje_6_8_0_preferido', 'viaje_11_8_1_preferido', 'viaje_26_8_5_preferido', 'viaje_1_8_7_preferido', 'viaje_1_9_0_8_7_preferido', 'viaje_25_9_2_6_preferido', 'viaje_10_9_1_preferido', 'viaje_4_9_3_preferido', 'viaje_13_9_4_preferido', 'viaje_19_9_5_preferido', 'viaje_2_3_1_5_preferido']
#sol = ['partido_4_8_12', 'partido_6_5_6', 'partido_0_1_10', 'partido_5_7_7', 'partido_5_3_14', 'partido_0_8_17', 'partido_7_2_14', 'partido_1_7_2', 'partido_8_7_19', 'partido_0_2_12', 'partido_9_8_11', 'partido_4_6_25', 'partido_6_1_16', 'partido_5_4_15', 'partido_6_4_10', 'partido_8_4_4', 'partido_0_9_4', 'partido_7_0_20', 'partido_8_1_8', 'partido_1_2_26', 'partido_3_1_25', 'partido_4_9_9', 'partido_6_3_21', 'partido_6_0_22', 'partido_3_8_10', 'partido_8_0_14', 'partido_5_0_26', 'partido_6_7_11', 'partido_3_2_0', 'partido_2_0_21', 'partido_1_9_14', 'partido_3_5_18', 'partido_2_6_18', 'partido_7_1_9', 'partido_1_8_6', 'partido_4_2_2', 'partido_5_1_3', 'partido_8_6_2', 'partido_2_4_11', 'partido_7_6_3', 'partido_3_4_26', 'partido_8_9_5', 'partido_0_6_1', 'partido_5_9_21', 'partido_9_7_15', 'partido_2_7_10', 'partido_1_3_15', 'partido_7_3_4', 'partido_7_9_6', 'partido_7_4_5', 'partido_9_3_7', 'partido_3_0_6', 'partido_7_5_23', 'partido_0_5_24', 'partido_9_5_20', 'partido_9_2_1', 'partido_9_1_24', 'partido_9_4_0', 'partido_6_2_20', 'partido_5_8_0', 'partido_9_6_26', 'partido_7_8_26', 'partido_8_3_3', 'partido_2_9_16', 'partido_6_9_17', 'partido_3_6_24', 'partido_3_9_12', 'partido_1_6_13', 'partido_1_4_20', 'partido_8_2_13', 'partido_0_3_2', 'partido_8_5_22', 'partido_4_0_7', 'partido_4_1_23', 'partido_4_5_19', 'partido_1_0_0', 'partido_2_8_24', 'partido_2_5_5', 'partido_4_3_8', 'partido_2_3_22', 'partido_0_7_25', 'partido_1_5_12', 'partido_0_4_3', 'partido_9_0_8', 'partido_6_8_23', 'partido_5_2_8', 'partido_4_7_16', 'partido_3_7_17', 'partido_5_6_9', 'partido_2_1_17', 'viaje_21_0_2_6_preferido', 'viaje_6_0_3_4_9_preferido', 'viaje_0_0_1_preferido', 'viaje_26_0_5_preferido', 'viaje_20_0_7_preferido', 'viaje_14_0_8_preferido', 'viaje_8_1_8_7_0_preferido', 'viaje_16_1_6_2_preferido', 'viaje_23_1_4_9_3_preferido', 'viaje_3_1_5_preferido', 'viaje_12_2_0_8_7_preferido', 'viaje_0_2_3_9_4_preferido', 'viaje_26_2_1_preferido', 'viaje_8_2_5_preferido', 'viaje_20_2_6_preferido', 'viaje_2_3_0_8_7_preferido', 'viaje_21_3_6_2_preferido', 'viaje_7_3_9_4_preferido', 'viaje_3_4_0_8_7_preferido', 'viaje_10_4_6_2_4_preferido', 'viaje_20_4_1_preferido', 'viaje_26_4_3_preferido', 'viaje_15_4_5_preferido', 'viaje_0_4_9_preferido', 'viaje_22_5_8_7_0_preferido', 'viaje_5_5_2_6_preferido', 'viaje_18_5_3_4_9_preferido', 'viaje_12_5_1_preferido', 'viaje_1_6_0_8_7_preferido', 'viaje_24_6_3_4_9_preferido', 'viaje_13_6_1_preferido', 'viaje_18_6_2_preferido', 'viaje_9_6_5_preferido', 'viaje_10_7_2_6_preferido', 'viaje_15_7_9_4_3_preferido', 'viaje_25_7_0_preferido', 'viaje_2_7_1_preferido', 'viaje_7_7_5_preferido', 'viaje_19_7_8_preferido', 'viaje_23_8_6_2_preferido', 'viaje_10_8_3_9_4_preferido', 'viaje_17_8_0_preferido', 'viaje_6_8_1_preferido', 'viaje_0_8_5_preferido', 'viaje_26_8_7_preferido', 'viaje_4_9_0_8_7_preferido', 'viaje_16_9_2_6_preferido', 'viaje_14_9_1_preferido', 'viaje_12_9_3_preferido', 'viaje_9_9_4_preferido', 'viaje_21_9_5_preferido', 'viaje_14_3_5_1_preferido']
#sol = ['partido_4_5_6', 'partido_8_0_22', 'partido_6_5_21', 'partido_2_7_14', 'partido_0_4_8', 'partido_8_7_20', 'partido_1_5_16', 'partido_3_4_15', 'partido_8_5_10', 'partido_6_1_9', 'partido_5_6_2', 'partido_0_3_10', 'partido_8_4_9', 'partido_5_1_14', 'partido_8_1_5', 'partido_6_4_4', 'partido_8_9_8', 'partido_7_8_6', 'partido_8_3_11', 'partido_9_1_21', 'partido_3_1_20', 'partido_3_6_22', 'partido_7_1_4', 'partido_9_5_5', 'partido_9_2_3', 'partido_6_8_26', 'partido_2_4_5', 'partido_7_3_12', 'partido_7_2_18', 'partido_2_6_11', 'partido_9_6_24', 'partido_2_1_10', 'partido_2_9_17', 'partido_0_2_20', 'partido_1_6_6', 'partido_2_5_22', 'partido_1_9_11', 'partido_1_7_7', 'partido_4_9_16', 'partido_1_8_24', 'partido_5_2_8', 'partido_5_0_17', 'partido_9_0_12', 'partido_1_2_26', 'partido_3_8_14', 'partido_6_7_13', 'partido_1_0_1', 'partido_5_4_26', 'partido_7_5_11', 'partido_9_8_13', 'partido_4_3_25', 'partido_2_8_25', 'partido_4_8_12', 'partido_4_1_22', 'partido_4_7_1', 'partido_3_5_7', 'partido_0_9_7', 'partido_5_3_19', 'partido_5_8_18', 'partido_5_7_25', 'partido_4_2_2', 'partido_8_2_19', 'partido_7_9_9', 'partido_0_6_15', 'partido_6_9_18', 'partido_7_6_17', 'partido_6_0_5', 'partido_9_3_26', 'partido_1_3_18', 'partido_0_8_2', 'partido_1_4_19', 'partido_0_1_3', 'partido_3_0_13', 'partido_0_7_26', 'partido_8_6_16', 'partido_3_9_23', 'partido_3_7_0', 'partido_4_6_23', 'partido_2_3_4', 'partido_0_5_9', 'partido_9_4_20', 'partido_7_0_23', 'partido_9_7_2', 'partido_7_4_10', 'partido_5_9_1', 'partido_4_0_11', 'partido_2_0_6', 'partido_6_3_3', 'partido_6_2_12', 'partido_3_2_1', 'viaje_5_0_6_2_preferido', 'viaje_11_0_4_9_3_preferido', 'viaje_1_0_1_preferido', 'viaje_17_0_5_preferido', 'viaje_23_0_7_preferido', 'viaje_22_0_8_preferido', 'viaje_3_1_0_7_8_preferido', 'viaje_9_1_6_2_preferido', 'viaje_20_1_3_9_4_preferido', 'viaje_14_1_5_preferido', 'viaje_18_2_7_8_0_preferido', 'viaje_1_2_3_4_9_preferido', 'viaje_26_2_1_preferido', 'viaje_8_2_5_preferido', 'viaje_12_2_6_preferido', 'viaje_10_3_0_8_7_preferido', 'viaje_3_3_6_2_preferido', 'viaje_25_3_4_9_preferido', 'viaje_8_4_0_8_7_preferido', 'viaje_4_4_6_2_preferido', 'viaje_19_4_1_preferido', 'viaje_15_4_3_preferido', 'viaje_26_4_5_preferido', 'viaje_20_4_9_preferido', 'viaje_9_5_0_8_7_preferido', 'viaje_21_5_6_2_preferido', 'viaje_5_5_9_4_3_preferido', 'viaje_16_5_1_preferido', 'viaje_15_6_0_8_7_preferido', 'viaje_22_6_3_4_9_preferido', 'viaje_6_6_1_preferido', 'viaje_11_6_2_preferido', 'viaje_2_6_5_preferido', 'viaje_13_7_6_2_preferido', 'viaje_0_7_3_4_9_preferido', 'viaje_26_7_0_preferido', 'viaje_7_7_1_preferido', 'viaje_25_7_5_preferido', 'viaje_20_7_8_preferido', 'viaje_25_8_2_6_preferido', 'viaje_12_8_4_9_3_preferido', 'viaje_2_8_0_preferido', 'viaje_24_8_1_preferido', 'viaje_18_8_5_preferido', 'viaje_6_8_7_preferido', 'viaje_7_9_0_8_7_preferido', 'viaje_16_9_4_2_6_preferido', 'viaje_11_9_1_preferido', 'viaje_23_9_3_preferido', 'viaje_1_9_5_preferido', 'viaje_18_3_1_5_preferido']
#sol = ['partido_8_4_3', 'partido_1_8_18', 'partido_7_6_24', 'partido_0_3_10', 'partido_4_7_6', 'partido_3_9_24', 'partido_4_0_13', 'partido_7_0_18', 'partido_8_9_9', 'partido_3_1_21', 'partido_0_8_26', 'partido_6_8_20', 'partido_1_4_8', 'partido_3_4_20', 'partido_9_4_26', 'partido_8_7_0', 'partido_6_2_7', 'partido_2_9_3', 'partido_3_8_13', 'partido_6_7_15', 'partido_1_2_24', 'partido_5_3_3', 'partido_1_7_13', 'partido_9_7_5', 'partido_3_7_7', 'partido_3_2_1', 'partido_0_5_20', 'partido_1_0_3', 'partido_7_3_12', 'partido_8_1_10', 'partido_9_6_18', 'partido_5_2_9', 'partido_1_9_1', 'partido_8_3_11', 'partido_7_2_17', 'partido_4_2_22', 'partido_5_7_26', 'partido_5_0_23', 'partido_8_2_16', 'partido_8_5_21', 'partido_7_9_10', 'partido_3_5_6', 'partido_5_8_2', 'partido_2_6_4', 'partido_0_2_15', 'partido_2_1_5', 'partido_7_1_11', 'partido_2_8_19', 'partido_6_5_12', 'partido_5_1_17', 'partido_4_6_17', 'partido_6_4_9', 'partido_9_8_15', 'partido_9_2_23', 'partido_9_5_4', 'partido_1_3_4', 'partido_0_1_9', 'partido_4_9_21', 'partido_2_7_14', 'partido_5_6_10', 'partido_6_3_25', 'partido_2_3_26', 'partido_9_1_22', 'partido_1_6_26', 'partido_4_8_14', 'partido_4_5_5', 'partido_5_4_15', 'partido_0_9_8', 'partido_6_0_1', 'partido_3_6_16', 'partido_4_3_18', 'partido_0_4_4', 'partido_0_6_22', 'partido_2_0_2', 'partido_0_7_21', 'partido_9_3_19', 'partido_9_0_12', 'partido_7_4_2', 'partido_2_5_13', 'partido_5_9_16', 'partido_6_9_2', 'partido_8_6_23', 'partido_1_5_14', 'partido_8_0_6', 'partido_2_4_10', 'partido_7_5_22', 'partido_7_8_8', 'partido_6_1_6', 'partido_4_1_23', 'partido_3_0_14', 'viaje_1_0_6_2_1_preferido', 'viaje_12_0_9_4_3_preferido', 'viaje_23_0_5_preferido', 'viaje_18_0_7_preferido', 'viaje_6_0_8_preferido', 'viaje_9_1_0_8_7_preferido', 'viaje_5_1_2_6_preferido', 'viaje_21_1_3_9_4_preferido', 'viaje_17_1_5_preferido', 'viaje_15_2_0_8_7_preferido', 'viaje_22_2_4_9_1_preferido', 'viaje_1_2_3_preferido', 'viaje_9_2_5_preferido', 'viaje_7_2_6_preferido', 'viaje_10_3_0_8_7_preferido', 'viaje_25_3_6_2_preferido', 'viaje_18_3_4_9_preferido', 'viaje_2_4_7_8_0_preferido', 'viaje_8_4_1_6_2_preferido', 'viaje_20_4_3_preferido', 'viaje_15_4_5_preferido', 'viaje_26_4_9_preferido', 'viaje_20_5_0_8_7_preferido', 'viaje_12_5_6_2_1_preferido', 'viaje_4_5_9_4_3_preferido', 'viaje_22_6_0_8_7_preferido', 'viaje_16_6_3_4_9_preferido', 'viaje_26_6_1_preferido', 'viaje_4_6_2_preferido', 'viaje_10_6_5_preferido', 'viaje_13_7_1_2_6_preferido', 'viaje_5_7_9_4_3_preferido', 'viaje_21_7_0_preferido', 'viaje_26_7_5_preferido', 'viaje_0_7_8_preferido', 'viaje_18_8_1_2_6_preferido', 'viaje_13_8_3_4_9_preferido', 'viaje_26_8_0_preferido', 'viaje_2_8_5_preferido', 'viaje_8_8_7_preferido', 'viaje_8_9_0_8_7_preferido', 'viaje_1_9_1_6_2_preferido', 'viaje_24_9_3_preferido', 'viaje_21_9_4_preferido', 'viaje_16_9_5_preferido', 'viaje_3_3_5_1_preferido']
#sol = ['partido_9_7_8', 'partido_2_1_11', 'partido_3_8_7', 'partido_1_8_13', 'partido_5_8_10', 'partido_6_0_17', 'partido_9_2_14', 'partido_0_3_4', 'partido_1_6_14', 'partido_7_2_1', 'partido_3_7_9', 'partido_8_5_4', 'partido_1_5_22', 'partido_6_9_4', 'partido_7_1_26', 'partido_7_3_2', 'partido_2_3_10', 'partido_7_0_11', 'partido_9_6_24', 'partido_5_7_25', 'partido_8_3_3', 'partido_8_4_15', 'partido_4_0_1', 'partido_2_6_8', 'partido_7_9_10', 'partido_0_8_26', 'partido_9_4_21', 'partido_5_1_18', 'partido_2_9_5', 'partido_5_0_8', 'partido_6_4_10', 'partido_6_8_23', 'partido_9_8_6', 'partido_8_2_2', 'partido_4_3_18', 'partido_1_4_0', 'partido_3_1_5', 'partido_0_9_12', 'partido_6_1_12', 'partido_4_6_25', 'partido_3_4_24', 'partido_2_5_16', 'partido_6_7_22', 'partido_4_2_13', 'partido_3_9_19', 'partido_4_8_5', 'partido_7_4_14', 'partido_7_8_17', 'partido_8_9_11', 'partido_5_6_2', 'partido_8_6_19', 'partido_7_5_5', 'partido_4_9_26', 'partido_6_3_11', 'partido_1_2_20', 'partido_9_1_7', 'partido_9_0_2', 'partido_9_5_13', 'partido_5_2_26', 'partido_2_0_18', 'partido_9_3_17', 'partido_3_0_0', 'partido_1_9_15', 'partido_2_8_24', 'partido_3_5_14', 'partido_0_1_24', 'partido_0_6_20', 'partido_2_4_9', 'partido_7_6_18', 'partido_2_7_21', 'partido_5_3_20', 'partido_1_0_9', 'partido_1_3_21', 'partido_8_7_0', 'partido_1_7_3', 'partido_4_5_12', 'partido_0_5_6', 'partido_6_5_15', 'partido_0_2_3', 'partido_3_2_15', 'partido_8_1_25', 'partido_4_1_6', 'partido_5_9_23', 'partido_0_4_16', 'partido_8_0_21', 'partido_5_4_3', 'partido_6_2_7', 'partido_4_7_7', 'partido_3_6_26', 'partido_0_7_15', 'viaje_17_0_6_2_preferido', 'viaje_0_0_3_4_9_preferido', 'viaje_9_0_1_preferido', 'viaje_8_0_5_preferido', 'viaje_11_0_7_preferido', 'viaje_21_0_8_preferido', 'viaje_24_1_0_8_7_preferido', 'viaje_11_1_2_6_preferido', 'viaje_5_1_3_4_9_preferido', 'viaje_18_1_5_preferido', 'viaje_1_2_7_8_0_preferido', 'viaje_13_2_4_9_3_preferido', 'viaje_20_2_1_preferido', 'viaje_26_2_5_preferido', 'viaje_7_2_6_preferido', 'viaje_2_3_7_8_0_preferido', 'viaje_10_3_2_6_preferido', 'viaje_17_3_9_4_preferido', 'viaje_14_4_7_8_0_preferido', 'viaje_9_4_2_6_preferido', 'viaje_0_4_1_preferido', 'viaje_24_4_3_preferido', 'viaje_3_4_5_preferido', 'viaje_21_4_9_preferido', 'viaje_4_5_8_7_0_preferido', 'viaje_15_5_6_2_preferido', 'viaje_12_5_4_9_3_preferido', 'viaje_22_5_1_preferido', 'viaje_18_6_7_8_0_preferido', 'viaje_24_6_9_4_3_preferido', 'viaje_14_6_1_preferido', 'viaje_8_6_2_preferido', 'viaje_2_6_5_preferido', 'viaje_21_7_2_6_preferido', 'viaje_7_7_4_9_3_preferido', 'viaje_15_7_0_preferido', 'viaje_3_7_1_preferido', 'viaje_25_7_5_preferido', 'viaje_0_7_8_preferido', 'viaje_23_8_6_2_preferido', 'viaje_5_8_4_9_3_preferido', 'viaje_26_8_0_preferido', 'viaje_13_8_1_preferido', 'viaje_10_8_5_preferido', 'viaje_17_8_7_preferido', 'viaje_10_9_7_8_0_preferido', 'viaje_4_9_6_2_preferido', 'viaje_15_9_1_preferido', 'viaje_19_9_3_preferido', 'viaje_26_9_4_preferido', 'viaje_23_9_5_preferido', 'viaje_20_3_5_1_preferido']

distancias = [[0, 967861, 412278, 1056566, 985275, 282954, 288800, 22976, 10361, 985275], 
              [967861, 0, 1040754, 1329495, 823584, 687319, 959697, 990833, 978194, 823584], 
              [412278, 1040754, 0, 648202, 709352, 518738, 133762, 413142, 411937, 709352], 
              [1056566, 1329495, 648202, 0, 567657, 1086393, 768103, 1059510, 1057264, 567657], 
              [985275, 823584, 709352, 567657, 0, 861070, 748467, 999869, 991365, 0], 
              [282954, 687319, 518738, 1086393, 861070, 0, 390469, 305840, 293308, 861070], 
              [288800, 959697, 133762, 768103, 748467, 390469, 0, 293318, 290057, 748467], 
              [22976, 990833, 413142, 1059510, 999869, 305840, 293318, 0, 12644, 999869], 
              [10361, 978194, 411937, 1057264, 991365, 293308, 290057, 12644, 0, 991365], 
              [985275, 823584, 709352, 567657, 0, 861070, 748467, 999869, 991365, 0]]


class fechaAmpliadaConLocalYVisitante:

	def __init__(self, local, visitante, nro_de_fecha_ampliada):
		self.local = local
		self.visitante = visitante
		self.nro_de_fecha_ampliada = nro_de_fecha_ampliada

	def get_local(self):
		return self.local
	def get_visitante(self):
		return self.visitante
	def get_nro_de_fecha_ampliada(self):
		return self.nro_de_fecha_ampliada	


class viajeConEquipoDestinosYFechaAmpliada:

	def __init__(self, equipo, lista_de_destinos, fecha_ampliada_de_inicio):
		self.equipo = equipo
		self.lista_de_destinos = lista_de_destinos
		self.fecha_ampliada_de_inicio = fecha_ampliada_de_inicio

	def get_equipo(self):
		return self.equipo
	def get_lista_de_destinos(self):
		return self.lista_de_destinos
	def get_fecha_ampliada_de_inicio(self):
		return self.fecha_ampliada_de_inicio

class viajeConEquipoDestinosYFecha:

	def __init__(self, equipo, lista_de_destinos, fecha_de_inicio):
		self.equipo = equipo
		self.lista_de_destinos = lista_de_destinos
		self.fecha_de_inicio = fecha_de_inicio

	def get_equipo(self):
		return self.equipo
	def get_lista_de_destinos(self):
		return self.lista_de_destinos
	def get_fecha_de_inicio(self):
		return self.fecha_de_inicio
	def tamaño(self):
		return (len(self.lista_de_destinos))
	def get_fecha_de_fin(self):
		return(self.fecha_de_inicio + self.tamaño() - 1)
	def kilometros(self):
		siguiente = self.equipo
		km = 0
		for i in self.lista_de_destinos:
			anterior = siguiente
			siguiente = i
			km = km + distancias[anterior][siguiente]
		anterior = siguiente
		siguiente = self.equipo
		km = km + distancias[anterior][siguiente]
		return km



sol_partidos = []
sol_viajes = []
for variable in sol:
       nombre = variable.rsplit("_")
       if nombre[0] == "partido":
              sol_partidos.append(fechaAmpliadaConLocalYVisitante(int(nombre[1]), int(nombre[2]), int(nombre[3])))
       else:
              if 0 ==0:#if nombre[-1] == "preferido":
                     sol_viajes.append(viajeConEquipoDestinosYFechaAmpliada(int(nombre[2]), [int(i) for i in nombre[3:-1]], int(nombre[1])))

def buscaindices(lista, sublista):
       esta = True
       indices = [i for i,e in enumerate(lista) if e == sublista[0]]
       for i in range(len(sublista)):
              esta = esta and (lista[indices[0] + i] == sublista [i])
       if esta:
              return range(indices[0], indices[0] + len(sublista))
       else:
              return range(indices[1], indices[1] + len(sublista))

def esSublista(lista,sublista):
	#Tamaño de sublista = 2
	indice = -1
	esta = False
	for i in range(len(lista)-1):
		if lista[i] == sublista[0]:
			if lista[i+1] == sublista[1]:
				esta = True
				indice = i
	return(esta, indice)

class equipoDeVolley:

	def __init__(self, nombre, indice):
		self.nombre = nombre
		self.indice = indice
		self.fechas = []
		self.fechas_ampliada = []
		self.localias = []
		self.localias_ampliada = []
		self.misma_cancha = set()
		self.preferencias = [False]*cantidad_de_dias
		self.rivales_por_dia = []
		self.viajes_por_dia = []
		self.ultima_fecha = False
		self.viajes_propios = []
		self.dias_por_fecha = []
		self.kilometros = 0

	def constructorDeFechas(self):
		if len(self.fechas) == 0:
			for k in range(cantidad_de_fechas_ampliada):
				self.fechas_ampliada.append(None)
				self.localias_ampliada.append(None)
				for solu in sol_partidos:
					if k == solu.get_nro_de_fecha_ampliada():
						if solu.get_visitante() == self.indice:
							self.fechas.append(solu.get_local())
							self.fechas_ampliada[k] = solu.get_local()
							self.localias.append(False)
							self.localias_ampliada[k] = False
							if k == cantidad_de_fechas_ampliada - 1:
								self.ultima_fecha = True
						elif int(solu.get_local()) == self.indice:
							self.fechas.append(solu.get_visitante())
							self.fechas_ampliada[k] = solu.get_visitante()
							self.localias.append(True)
							self.localias_ampliada[k] = True
							if k == cantidad_de_fechas_ampliada - 1:
								self.ultima_fecha = True

	def constructorDeViajes(self):	
		if len(self.viajes_propios) == 0:
			self.constructorDeFechas()
			contador = 0
			for k in range(cantidad_de_fechas_ampliada):
				for solu in sol_viajes:
					if k == solu.get_fecha_ampliada_de_inicio():
						if solu.get_equipo() == self.indice:
							for i in range(cantidad_de_fechas):
								if (self.get_fechas_ampliada()[solu.get_fecha_ampliada_de_inicio()] == self.get_fechas()[i] and self.get_localias()[i] == False):
									indice = i
							if len(solu.get_lista_de_destinos()) > 1:
								self.viajes_propios.append(viajeConEquipoDestinosYFecha(solu.get_equipo(), solu.get_lista_de_destinos(), indice))
							contador += 1


	def get_fechas(self):
		#devuelve lista de tamaño cantidad_de_fechas
		self.constructorDeFechas()
		return self.fechas

	def get_fechas_ampliada(self):
		#devuelve lista de tamaño cantidad_de_fechas
		self.constructorDeFechas()
		return self.fechas_ampliada

	def get_localias(self):
		#devuelve lista de tamaño cantidad_de_fechas
		self.constructorDeFechas()
		return self.localias

	def get_localias_ampliada(self):
		#devuelve lista de tamaño cantidad_de_fechas
		self.constructorDeFechas()
		return self.localias_ampliada

	def get_viajes_propios(self):
		self.constructorDeViajes()
		return self.viajes_propios

	# def get_viajes(self):
	# 	#devuelve lista de tamaño cantidad_de_fechas
	# 	if len(self.viajes) == 0:
	# 		self.constructorDeViajes()
	# 	return self.viajes

	# def estaDeViajeEnFecha(self, fecha):
	# 	return (self.get_viajes()[fecha] == 1)

	def estaDeViajeEnFechaYEnSiguiente(self, fecha):
		self.constructorDeViajes()
		for viaje in self.viajes_propios:
			if (viaje.get_fecha_de_inicio() <= fecha) and (fecha <= viaje.get_fecha_de_fin()):
				[esta, indice] = esSublista(viaje.get_lista_de_destinos(), self.get_fechas()[fecha:fecha+2])
				if esta and (viaje.get_fecha_de_inicio() + indice == fecha):
					return True
		return False

	def estaDeViajeEnFecha(self, fecha):
		if self.juegaDeLocalEnFecha(fecha):
			return False
		else:
			for viaje in self.get_viajes_propios():
				if self.get_fechas()[fecha] in viaje.get_lista_de_destinos():
					return True
		return False

	def comienzaViajeEnFecha(self, fecha):
		rv = False
		for viaje in self.get_viajes_propios():
			rv = rv or (viaje.get_fecha_de_inicio() == fecha)
		return rv

	def finalizaViajeEnFecha(self, fecha):
		rv = False
		for viaje in self.get_viajes_propios():
			rv = rv or (viaje.get_fecha_de_fin() == fecha)
		return rv

	def esPartidoDeIda(self, fecha):
		return (self.get_fechas().index(self.get_fechas()[fecha]) == fecha)

	def juegaContraEnFechas(self, otroEquipo, fechaPropia, fechaAjena):
		return(self.get_fechas()[fechaPropia] == otroEquipo.indice and 
			otroEquipo.get_fechas()[fechaAjena] == self.indice and 
			(self.esPartidoDeIda(fechaPropia) == otroEquipo.esPartidoDeIda(fechaAjena)))

	def juegaDeLocalEnFecha(self, fecha):
		return self.get_localias()[fecha]

	def set_comparteCancha(self, otroEquipo):
		self.misma_cancha.add(otroEquipo)
		otroEquipo.misma_cancha.add(self)

	def comparteCancha(self, otroEquipo):
		return otroEquipo in self.misma_cancha

	def preferenciaLocalEnDia(self, dia):
		return self.preferencias[dia]

	def set_preferenciasLocal(self, lista):
		self.preferencias = lista

	def juega_en_la_ultima_fecha(self):
		self.constructorDeFechas()
		return self.ultima_fecha

	def set_rivales_por_dia(self, lista):
		##lista de listas con [equipo, fecha, dia]
		if len(self.rivales_por_dia) == 0:
			self.rivales_por_dia = [0]*cantidad_de_dias
			self.dias_por_fecha = [0]*cantidad_de_fechas
			for elemento in lista:
				dia = elemento[2]
				fecha = elemento[1]
				equipo = elemento[0]
				if equipo == self.indice:
					self.dias_por_fecha[fecha] = dia
					rival = Equipos[self.get_fechas()[fecha]]
					if self.juegaDeLocalEnFecha(fecha):
						self.rivales_por_dia[dia] = (rival, 'local')
					else:
						self.rivales_por_dia[dia] = (rival, 'visitante')
			self.set_viajes_por_dias()

	def get_rivales_por_dia(self):
		return self.rivales_por_dia

	def set_viajes_por_dias(self):
		if len(self.viajes_por_dia) == 0:
			contador = -1
			de_viaje = False
			for k in range(cantidad_de_dias):
				self.viajes_por_dia.append(de_viaje)
				if self.rivales_por_dia[k] != 0:
					contador += 1
					de_viaje = self.estaDeViajeEnFechaYEnSiguiente(contador)
					if self.estaDeViajeEnFechaYEnSiguiente(contador):
						self.viajes_por_dia[k] = True

	def get_viajes_por_dia(self):
		return self.viajes_por_dia
	def visitante_sin_viaje_en_fecha(self, i):
		if self.juegaDeLocalEnFecha(i) or self.estaDeViajeEnFecha(i):
			return False
		else:
			return True

	def get_dia_en_que_juega_fecha(self,indice):
		return self.dias_por_fecha[indice]

	def get_kilometros(self):
		if self.kilometros ==0:
			viajes = self.get_viajes_propios()
			for viaje in viajes:
				print(viaje.lista_de_destinos, viaje.kilometros())
				self.kilometros += viaje.kilometros()
			for i in range(cantidad_de_fechas):
				if self.visitante_sin_viaje_en_fecha(i):
					print(i, self.indice)
					self.kilometros += 2*distancias[self.indice][self.get_fechas()[i]]
		return self.kilometros

	








Equipos = [
equipoDeVolley("Ciudad", 0),
equipoDeVolley("Gigantes", 1),
equipoDeVolley("Libertad", 2),
equipoDeVolley("Monteros", 3),
equipoDeVolley("Obras", 4),
equipoDeVolley("Bolivar", 5),
equipoDeVolley("PSM", 6),
equipoDeVolley("River", 7),
equipoDeVolley("UnTreF", 8),
equipoDeVolley("UPCN", 9)]


Equipos[4].set_comparteCancha(Equipos[9])
print([i.get_kilometros() for i in Equipos])
print(sum([i.get_kilometros() for i in Equipos]))
#solucion = [[0, 0, 7], [0, 1, 9], [0, 2, 13], [0, 3, 19], [0, 4, 22], [0, 5, 27], [0, 6, 32], [0, 7, 34], [0, 8, 38], [0, 9, 40], [0, 10, 42], [0, 11, 44], [0, 12, 46], [0, 13, 50], [0, 14, 52], [0, 15, 54], [0, 16, 59], [0, 17, 62], [0, 18, 67], [0, 19, 69], [1, 0, 6], [1, 1, 9], [1, 2, 13], [1, 3, 19], [1, 4, 25], [1, 5, 27], [1, 6, 30], [1, 7, 33], [1, 8, 35], [1, 9, 39], [1, 10, 42], [1, 11, 44], [1, 12, 48], [1, 13, 51], [1, 14, 54], [1, 15, 59], [1, 16, 61], [1, 17, 63], [1, 18, 65], [1, 19, 69], [2, 0, 1], [2, 1, 4], [2, 2, 7], [2, 3, 9], [2, 4, 13], [2, 5, 18], [2, 6, 25], [2, 7, 32], [2, 8, 34], [2, 9, 38], [2, 10, 40], [2, 11, 42], [2, 12, 47], [2, 13, 49], [2, 14, 54], [2, 15, 57], [2, 16, 61], [2, 17, 63], [2, 18, 67], [2, 19, 69], [3, 0, 6], [3, 1, 12], [3, 2, 15], [3, 3, 19], [3, 4, 21], [3, 5, 26], [3, 6, 28], [3, 7, 30], [3, 8, 35], [3, 9, 37], [3, 10, 40], [3, 11, 42], [3, 12, 48], [3, 13, 54], [3, 14, 56], [3, 15, 59], [3, 16, 61], [3, 17, 63], [3, 18, 67], [3, 19, 69], [4, 0, 4], [4, 1, 7], [4, 2, 13], [4, 3, 17], [4, 4, 19], [4, 5, 26], [4, 6, 28], [4, 7, 31], [4, 8, 34], [4, 9, 37], [4, 10, 40], [4, 11, 46], [4, 12, 48], [4, 13, 53], [4, 14, 57], [4, 15, 59], [4, 16, 61], [4, 17, 63], [4, 18, 65], [4, 19, 67], [5, 0, 4], [5, 1, 11], [5, 2, 18], [5, 3, 20], [5, 4, 26], [5, 5, 28], [5, 6, 31], [5, 7, 37], [5, 8, 40], [5, 9, 42], [5, 10, 44], [5, 11, 46], [5, 12, 48], [5, 13, 50], [5, 14, 54], [5, 15, 58], [5, 16, 61], [5, 17, 63], [5, 18, 65], [5, 19, 69], [6, 0, 7], [6, 1, 12], [6, 2, 15], [6, 3, 17], [6, 4, 19], [6, 5, 26], [6, 6, 30], [6, 7, 34], [6, 8, 36], [6, 9, 40], [6, 10, 42], [6, 11, 44], [6, 12, 47], [6, 13, 53], [6, 14, 56], [6, 15, 58], [6, 16, 60], [6, 17, 63], [6, 18, 65], [6, 19, 69], [7, 0, 6], [7, 1, 13], [7, 2, 17], [7, 3, 20], [7, 4, 25], [7, 5, 28], [7, 6, 31], [7, 7, 34], [7, 8, 36], [7, 9, 38], [7, 10, 40], [7, 11, 44], [7, 12, 47], [7, 13, 52], [7, 14, 54], [7, 15, 56], [7, 16, 59], [7, 17, 65], [7, 18, 67], [7, 19, 69], [8, 0, 6], [8, 1, 9], [8, 2, 13], [8, 3, 15], [8, 4, 17], [8, 5, 19], [8, 6, 25], [8, 7, 28], [8, 8, 33], [8, 9, 38], [8, 10, 42], [8, 11, 44], [8, 12, 46], [8, 13, 52], [8, 14, 54], [8, 15, 57], [8, 16, 59], [8, 17, 61], [8, 18, 63], [8, 19, 69], [9, 0, 4], [9, 1, 7], [9, 2, 11], [9, 3, 13], [9, 4, 17], [9, 5, 19], [9, 6, 22], [9, 7, 25], [9, 8, 30], [9, 9, 37], [9, 10, 40], [9, 11, 42], [9, 12, 44], [9, 13, 51], [9, 14, 54], [9, 15, 57], [9, 16, 62], [9, 17, 65], [9, 18, 67], [9, 19, 69], [10, 0, 1], [10, 1, 7], [10, 2, 13], [10, 3, 15], [10, 4, 17], [10, 5, 19], [10, 6, 21], [10, 7, 25], [10, 8, 28], [10, 9, 31], [10, 10, 34], [10, 11, 39], [10, 12, 44], [10, 13, 47], [10, 14, 49], [10, 15, 52], [10, 16, 56], [10, 17, 60], [10, 18, 63], [10, 19, 69]]

# Equipos[1].set_rivales_por_dia(solucion)
# for i in range(cantidad_de_dias):
# 	if Equipos[1].get_rivales_por_dia()[i] != 0:
# 		print(Equipos[1].get_rivales_por_dia()[i][0].indice)
# 	else:
# 		print(".")
#print(Equipos[1].get_fechas())
#print(Equipos[0].get_fechas_ampliada())
#print(Equipos[0].get_localias_ampliada())
#print([[i.get_fecha_de_inicio(), i.lista_de_destinos] for i in Equipos[1].get_viajes_propios()])
#print(Equipos[0].get_localias())
#print([Equipos[1].estaDeViajeEnFechaYEnSiguiente(i) for i in range(cantidad_de_fechas)])

# for i in Equipos:
# 	print([i.estaDeViajeEnFechaYEnSiguiente(j) for j in range(cantidad_de_fechas)])
# 	print([[j.get_fecha_de_inicio(), j.get_lista_de_destinos()] for j in i.get_viajes_propios()])
