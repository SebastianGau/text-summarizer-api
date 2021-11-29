# Databricks notebook source
import os
import pandas as pd
import numpy as np
import statistics


def load_standard_envs():
    os.environ["PUMP_HEAD_COUNT"] = "3"
    os.environ["PUMP_SHIFTFACTOR"] = "770"
    os.environ["PUMP_NORMAL_SHIFTFACTOR"] = "1200"
    os.environ["PUMP_VAR_P_DISCHARGE_MAX"] = "300"
    os.environ["PUMP_DP_PHASE_GRAD_MAX"] = "0.2"
    os.environ["PUMP_KPI_METADATA"] = """[
    {
        "Name": "ID",
        "Displayname": "CycleID",
        "Unit": null,
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    },
    {
        "Name": "servertime",
        "Displayname": "CylcletimeStart",
        "Unit": null,
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    },
    {
        "Name": "KPI_Cycle_Time",
        "Displayname": "Cycle_Time",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    },
    {
        "Name": "KPI_Cycle_TimeEnd",
        "Displayname": "Cycle_TimeEnd",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    },
    {
        "Name": "KPI_Cycle_TimeStart",
        "Displayname": "Cycle_TimeStart",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head1_Angle",
        "Displayname": "DischargePhase Angle lenght (angle)",
        "Unit": "grade",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head1_AngleEnd",
        "Displayname": "DischargePhase Angle End",
        "Unit": "grade",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head1_AngleStart",
        "Displayname": "DischargePhase Angle Start",
        "Unit": "grade",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head1_percentage",
        "Displayname": "DischargePhase lenght (%)",
        "Unit": "%",
        "Head": 1,
        "MINLIM": "37,6",
        "MAXLIM": "38,1",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head1_Pressure_max",
        "Displayname": "DischargePhase Pressure max",
        "Unit": "bar",
        "Head": 1,
        "MINLIM": "280",
        "MAXLIM": "300",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head1_Pressure_mean",
        "Displayname": "DischargePhase Pressure mean",
        "Unit": "bar",
        "Head": 1,
        "MINLIM": "260",
        "MAXLIM": "290",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head1_Pressure_min",
        "Displayname": "DischargePhase Pressure min",
        "Unit": "bar",
        "Head": 1,
        "MINLIM": "250",
        "MAXLIM": "270",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head1_Time",
        "Displayname": "DischargePhase Time lenght (ms)",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head1_TimeEnd",
        "Displayname": "DischargePhase Time End (ms)",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head1_TimeStart",
        "Displayname": "DischargePhase Time Start (ms)",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head2_Angle",
        "Displayname": "DischargePhase Angle lenght (angle)",
        "Unit": "grade",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head2_AngleEnd",
        "Displayname": "DischargePhase Angle End",
        "Unit": "grade",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head2_AngleStart",
        "Displayname": "DischargePhase Angle Start",
        "Unit": "grade",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head2_percentage",
        "Displayname": "DischargePhase lenght (%)",
        "Unit": "%",
        "Head": 2,
        "MINLIM": "36,2",
        "MAXLIM": "37",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head2_Pressure_max",
        "Displayname": "DischargePhase Pressure max",
        "Unit": "bar",
        "Head": 2,
        "MINLIM": "280",
        "MAXLIM": "300",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head2_Pressure_mean",
        "Displayname": "DischargePhase Pressure mean",
        "Unit": "bar",
        "Head": 2,
        "MINLIM": "260",
        "MAXLIM": "290",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head2_Pressure_min",
        "Displayname": "DischargePhase Pressure min",
        "Unit": "bar",
        "Head": 2,
        "MINLIM": "250",
        "MAXLIM": "270",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head2_Time",
        "Displayname": "DischargePhase Time lenght (ms)",
        "Unit": "ms",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head2_TimeEnd",
        "Displayname": "DischargePhase Time End (ms)",
        "Unit": "ms",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head2_TimeStart",
        "Displayname": "DischargePhase Time Start (ms)",
        "Unit": "ms",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head3_Angle",
        "Displayname": "DischargePhase Angle lenght (angle)",
        "Unit": "grade",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head3_AngleEnd",
        "Displayname": "DischargePhase Angle End",
        "Unit": "grade",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head3_AngleStart",
        "Displayname": "DischargePhase Angle Start",
        "Unit": "grade",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head3_percentage",
        "Displayname": "DischargePhase lenght (%)",
        "Unit": "%",
        "Head": 3,
        "MINLIM": "38",
        "MAXLIM": "38,3",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head3_Pressure_max",
        "Displayname": "DischargePhase Pressure max",
        "Unit": "bar",
        "Head": 3,
        "MINLIM": "280",
        "MAXLIM": "300",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head3_Pressure_mean",
        "Displayname": "DischargePhase Pressure mean",
        "Unit": "bar",
        "Head": 3,
        "MINLIM": "260",
        "MAXLIM": "290",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head3_Pressure_min",
        "Displayname": "DischargePhase Pressure min",
        "Unit": "bar",
        "Head": 3,
        "MINLIM": "250",
        "MAXLIM": "270",
        "DISPLAY": true
    },
    {
        "Name": "KPI_DischargePhase_Head3_Time",
        "Displayname": "DischargePhase Time lenght (ms)",
        "Unit": "ms",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head3_TimeEnd",
        "Displayname": "DischargePhase Time End (ms)",
        "Unit": "ms",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_DischargePhase_Head3_TimeStart",
        "Displayname": "DischargePhase Time Start (ms)",
        "Unit": "ms",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head1_Angle",
        "Displayname": "SniffingPhase Angle lenght (angle)",
        "Unit": "grade",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head1_AngleEnd",
        "Displayname": "SniffingPhase Angle End",
        "Unit": "grade",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head1_AngleStart",
        "Displayname": "SniffingPhase Angle Start",
        "Unit": "grade",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head1_percentage",
        "Displayname": "SniffingPhase lenght (%)",
        "Unit": "%",
        "Head": 1,
        "MINLIM": "3,4",
        "MAXLIM": "3,6",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head1_Pressure_max",
        "Displayname": "SniffingPhase Pressure max",
        "Unit": "bar",
        "Head": 1,
        "MINLIM": "5",
        "MAXLIM": "8",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head1_Pressure_mean",
        "Displayname": "SniffingPhase Pressure mean",
        "Unit": "bar",
        "Head": 1,
        "MINLIM": "4",
        "MAXLIM": "6",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head1_Pressure_min",
        "Displayname": "SniffingPhase Pressure min",
        "Unit": "bar",
        "Head": 1,
        "MINLIM": "3",
        "MAXLIM": "5",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head1_Time",
        "Displayname": "SniffingPhase Time lenght (ms)",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head1_TimeEnd",
        "Displayname": "SniffingPhase Time End (ms)",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head1_TimeStart",
        "Displayname": "SniffingPhase Time Start (ms)",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head2_Angle",
        "Displayname": "SniffingPhase Angle lenght (angle)",
        "Unit": "grade",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head2_AngleEnd",
        "Displayname": "SniffingPhase Angle End",
        "Unit": "grade",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head2_AngleStart",
        "Displayname": "SniffingPhase Angle Start",
        "Unit": "grade",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head2_percentage",
        "Displayname": "SniffingPhase lenght (%)",
        "Unit": "%",
        "Head": 2,
        "MINLIM": "4,4",
        "MAXLIM": "4,6",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head2_Pressure_max",
        "Displayname": "SniffingPhase Pressure max",
        "Unit": "bar",
        "Head": 2,
        "MINLIM": "5",
        "MAXLIM": "8",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head2_Pressure_mean",
        "Displayname": "SniffingPhase Pressure mean",
        "Unit": "bar",
        "Head": 2,
        "MINLIM": "4",
        "MAXLIM": "6",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head2_Pressure_min",
        "Displayname": "SniffingPhase Pressure min",
        "Unit": "bar",
        "Head": 2,
        "MINLIM": "3",
        "MAXLIM": "5",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head2_Time",
        "Displayname": "SniffingPhase Time lenght (ms)",
        "Unit": "ms",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head2_TimeEnd",
        "Displayname": "SniffingPhase Time End (ms)",
        "Unit": "ms",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head2_TimeStart",
        "Displayname": "SniffingPhase Time Start (ms)",
        "Unit": "ms",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head3_Angle",
        "Displayname": "SniffingPhase Angle lenght (angle)",
        "Unit": "grade",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head3_AngleEnd",
        "Displayname": "SniffingPhase Angle End",
        "Unit": "grade",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head3_AngleStart",
        "Displayname": "SniffingPhase Angle Start",
        "Unit": "grade",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head3_percentage",
        "Displayname": "SniffingPhase lenght (%)",
        "Unit": "%",
        "Head": 3,
        "MINLIM": "4,6",
        "MAXLIM": "4,8",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head3_Pressure_max",
        "Displayname": "SniffingPhase Pressure max",
        "Unit": "bar",
        "Head": 3,
        "MINLIM": "5",
        "MAXLIM": "8",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head3_Pressure_mean",
        "Displayname": "SniffingPhase Pressure mean",
        "Unit": "bar",
        "Head": 3,
        "MINLIM": "4",
        "MAXLIM": "6",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head3_Pressure_min",
        "Displayname": "SniffingPhase Pressure min",
        "Unit": "bar",
        "Head": 3,
        "MINLIM": "3",
        "MAXLIM": "5",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SniffingPhase_Head3_Time",
        "Displayname": "SniffingPhase Time lenght (ms)",
        "Unit": "ms",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head3_TimeEnd",
        "Displayname": "SniffingPhase Time End (ms)",
        "Unit": "ms",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SniffingPhase_Head3_TimeStart",
        "Displayname": "SniffingPhase Time Start (ms)",
        "Unit": "ms",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head1_Angle",
        "Displayname": "SuctionPhase Angle lenght (angle)",
        "Unit": "grade",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head1_AngleEnd",
        "Displayname": "SuctionPhase Angle End",
        "Unit": "grade",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head1_AngleStart",
        "Displayname": "SuctionPhase Angle Start",
        "Unit": "grade",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head1_percentage",
        "Displayname": "SuctionPhase lenght (%)",
        "Unit": "%",
        "Head": 1,
        "MINLIM": "32,9",
        "MAXLIM": "33,1",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head1_Pressure_max",
        "Displayname": "SuctionPhase Pressure max",
        "Unit": "bar",
        "Head": 1,
        "MINLIM": "10",
        "MAXLIM": "14",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head1_Pressure_mean",
        "Displayname": "SuctionPhase Pressure mean",
        "Unit": "bar",
        "Head": 1,
        "MINLIM": "5",
        "MAXLIM": "10",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head1_Pressure_min",
        "Displayname": "SuctionPhase Pressure min",
        "Unit": "bar",
        "Head": 1,
        "MINLIM": "3",
        "MAXLIM": "5",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head1_Time",
        "Displayname": "SuctionPhase Time lenght (ms)",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head1_TimeEnd",
        "Displayname": "SuctionPhase Time End (ms)",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head1_TimeStart",
        "Displayname": "SuctionPhase Time Start (ms)",
        "Unit": "ms",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head2_Angle",
        "Displayname": "SuctionPhase Angle lenght (angle)",
        "Unit": "grade",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head2_AngleEnd",
        "Displayname": "SuctionPhase Angle End",
        "Unit": "grade",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head2_AngleStart",
        "Displayname": "SuctionPhase Angle Start",
        "Unit": "grade",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head2_percentage",
        "Displayname": "SuctionPhase lenght (%)",
        "Unit": "%",
        "Head": 2,
        "MINLIM": "33",
        "MAXLIM": "33,2",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head2_Pressure_max",
        "Displayname": "SuctionPhase Pressure max",
        "Unit": "bar",
        "Head": 2,
        "MINLIM": "10",
        "MAXLIM": "14",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head2_Pressure_mean",
        "Displayname": "SuctionPhase Pressure mean",
        "Unit": "bar",
        "Head": 2,
        "MINLIM": "5",
        "MAXLIM": "10",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head2_Pressure_min",
        "Displayname": "SuctionPhase Pressure min",
        "Unit": "bar",
        "Head": 2,
        "MINLIM": "3",
        "MAXLIM": "5",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head2_Time",
        "Displayname": "SuctionPhase Time lenght (ms)",
        "Unit": "ms",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head2_TimeEnd",
        "Displayname": "SuctionPhase Time End (ms)",
        "Unit": "ms",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head2_TimeStart",
        "Displayname": "SuctionPhase Time Start (ms)",
        "Unit": "ms",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head3_Angle",
        "Displayname": "SuctionPhase Angle lenght (angle)",
        "Unit": "grade",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head3_AngleEnd",
        "Displayname": "SuctionPhase Angle End",
        "Unit": "grade",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head3_AngleStart",
        "Displayname": "SuctionPhase Angle Start",
        "Unit": "grade",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head3_percentage",
        "Displayname": "SuctionPhase lenght (%)",
        "Unit": "%",
        "Head": 3,
        "MINLIM": "32,5",
        "MAXLIM": "32,7",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head3_Pressure_max\"",
        "Displayname": "SuctionPhase Pressure max",
        "Unit": "bar",
        "Head": 3,
        "MINLIM": "10",
        "MAXLIM": "14",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head3_Pressure_mean",
        "Displayname": "SuctionPhase Pressure mean",
        "Unit": "bar",
        "Head": 3,
        "MINLIM": "5",
        "MAXLIM": "10",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head3_Pressure_min",
        "Displayname": "SuctionPhase Pressure min",
        "Unit": "bar",
        "Head": 3,
        "MINLIM": "3",
        "MAXLIM": "5",
        "DISPLAY": true
    },
    {
        "Name": "KPI_SuctionPhase_Head3_Time",
        "Displayname": "SuctionPhase Time lenght (ms)",
        "Unit": "ms",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head3_TimeEnd",
        "Displayname": "SuctionPhase Time End (ms)",
        "Unit": "ms",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SuctionPhase_Head3_TimeStart",
        "Displayname": "SuctionPhase Time Start (ms)",
        "Unit": "ms",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": false
    },
    {
        "Name": "KPI_SolideBorneNoice_Head1_Variance",
        "Displayname": "SolideBorneNoice Variance",
        "Unit": "dB",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    },
    {
        "Name": "KPI_SolideBorneNoice_Head2_Variance",
        "Displayname": "SolideBorneNoice Variance",
        "Unit": "dB",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    },
    {
        "Name": "KPI_SolideBorneNoice_Head3_Variance",
        "Displayname": "SolideBorneNoice Variance",
        "Unit": "dB",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    },
    {
        "Name": "KPI_SolideBorneNoice_Head1_mean",
        "Displayname": "SolideBorneNoice Mean",
        "Unit": "dB",
        "Head": 1,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    },
    {
        "Name": "KPI_SolideBorneNoice_Head2_mean",
        "Displayname": "SolideBorneNoice Mean",
        "Unit": "dB",
        "Head": 2,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    },
    {
        "Name": "KPI_SolideBorneNoice_Head3_mean",
        "Displayname": "SolideBorneNoice Mean",
        "Unit": "dB",
        "Head": 3,
        "MINLIM": null,
        "MAXLIM": null,
        "DISPLAY": true
    }
]"""

if not "PUMP_HEAD_COUNT" in os.environ:
    load_standard_envs()

# Variables for a spezific pump
config = dict()
config["numHeads"] = int(os.environ["PUMP_HEAD_COUNT"])

# shifting_variables:
# factor for the right startpoint
var_shiftfactor = int(os.environ["PUMP_SHIFTFACTOR"])
# shift Data from Head 1 and 3
var_normal_shiftfactor = int(os.environ["PUMP_NORMAL_SHIFTFACTOR"])
var_p_discharge_max = int(os.environ["PUMP_VAR_P_DISCHARGE_MAX"])
dp_phase_grad_max = float(os.environ["PUMP_DP_PHASE_GRAD_MAX"])

config.update(
    {
        "shiftHeads": [
            var_shiftfactor + var_normal_shiftfactor,
            var_shiftfactor,
            var_shiftfactor - var_normal_shiftfactor,
        ],
        "mavg_steps": 50,
        "p_discharge_lim": var_p_discharge_max / 2,
        "DPhaseMin": var_p_discharge_max - 50,
        "DPhaseGradMax": dp_phase_grad_max,
    }
)
config["DPhaseGradMin"] = -config["DPhaseGradMax"]


def data_prep(df: pd.DataFrame) -> pd.DataFrame:
    # init output df
    df_out = pd.DataFrame()

    # assign Angle
    df_out["Angle"] = df["2:Angle"]
    df_out["Timestamp"] = pd.to_datetime(df["2:Timestamps"])

    # shifting Data, moving average and gradient_calc
    i = 1
    for shift in config["shiftHeads"]:
        # shifting
        df_out["s_PressureHead" + str(i)] = np.roll(df["2:PressureHead" + str(i)], shift)
        df_out["s_VibrationHead" + str(i)] = np.roll(df["2:VibrationHead" + str(i)], shift)

        # moving average
        df_out["s_PressureHead" + str(i) + "avg"] = (
            df_out["s_PressureHead" + str(i)].rolling(config["mavg_steps"]).mean()
        )

        # gradients
        df_out["s_PressureHead" + str(i) + "avg_grd"] = np.gradient(
            df_out["s_PressureHead" + str(i) + "avg"]
        )
        i = i + 1

    return df_out


def vibration_full(df: pd.DataFrame) -> pd.DataFrame:
    out = dict()
    for i in range(1, config["numHeads"] + 1):
        out["KPI_SolideBorneNoice_Head" + str(i) + "_Variance"] = df.loc[:,["s_VibrationHead" + str(i)]].var()
        out["KPI_SolideBorneNoice_Head" + str(i) + "_mean"] = statistics.mean(df["s_VibrationHead" + str(i)])
    return out


def eval_DPhase(df: pd.DataFrame) -> pd.DataFrame:
    out = dict()
    for i in range(1, config["numHeads"] + 1):
        # determine Discharge Phase Dataset
        df_DPhase = df[
            (df["s_PressureHead" + str(i)] > config["DPhaseMin"])
            & (df["s_PressureHead" + str(i) + "avg_grd"] < config["DPhaseGradMax"])
            & (df["s_PressureHead" + str(i) + "avg_grd"] > config["DPhaseGradMin"])
        ]
        # basic statistics
        out["KPI_DischargePhase_Head" + str(i) + "_Pressure_mean"] = statistics.mean(
            df_DPhase["s_PressureHead" + str(i) + "avg"]
        )
        out["KPI_DischargePhase_Head" + str(i) + "_Pressure_min"] = df_DPhase[
            "s_PressureHead" + str(i) + "avg"
        ].min()
        out["KPI_DischargePhase_Head" + str(i) + "_Pressure_max"] = df_DPhase[
            "s_PressureHead" + str(i) + "avg"
        ].max()

        # start, end, duration
        out["KPI_DischargePhase_Head" + str(i) + "_TimeStart"] = df_DPhase.iloc[0]["Timestamp"]
        out["KPI_DischargePhase_Head" + str(i) + "_AngleStart"] = df_DPhase.iloc[0]["Angle"]

        out["KPI_DischargePhase_Head" + str(i) + "_TimeEnd"] = df_DPhase.iloc[-1]["Timestamp"]
        out["KPI_DischargePhase_Head" + str(i) + "_AngleEnd"] = df_DPhase.iloc[-1]["Angle"]

        out["KPI_DischargePhase_Head" + str(i) + "_Time"] = (
            out["KPI_DischargePhase_Head" + str(i) + "_TimeEnd"]
            - out["KPI_DischargePhase_Head" + str(i) + "_TimeStart"]
        )
        out["KPI_DischargePhase_Head" + str(i) + "_Angle"] = len(
            df_DPhase
        )  # /10 ?? why not end-start?
        # fraction of full cycle
        out["KPI_DischargePhase_Head" + str(i) + "_percentage"] = (
            out["KPI_DischargePhase_Head" + str(i) + "_Angle"] / 3600 * 100
        )

    return out


def eval_SnSuPhase(df: pd.DataFrame) -> pd.DataFrame:
    out = dict()
    for i in range(1, config["numHeads"] + 1):
        # determine Sniffing&SuctionPhase df
        # might want to use PressureHeadavg in first condition?
        df_SnSuPhase = df[
            (df["s_PressureHead" + str(i)] < config["p_discharge_lim"])
            & (df["s_PressureHead" + str(i) + "avg_grd"] < config["DPhaseGradMax"])
            & (df["s_PressureHead" + str(i) + "avg_grd"] > config["DPhaseGradMin"])
        ]

        # calc mean für Suction and Sniffing phase (Pressure)
        SnSuPhase_P_mean = statistics.mean(df_SnSuPhase["s_PressureHead" + str(i) + "avg"])

        # SniffingPhase
        df_SnPhase = df_SnSuPhase[
            (df_SnSuPhase["s_PressureHead" + str(i) + "avg"] < SnSuPhase_P_mean * 0.7)
        ]

        # basic statistics
        out["KPI_SniffingPhase_Head" + str(i) + "_Pressure_mean"] = statistics.mean(
            df_SnPhase["s_PressureHead" + str(i) + "avg"]
        )
        out["KPI_SniffingPhase_Head" + str(i) + "_Pressure_min"] = df_SnPhase[
            "s_PressureHead" + str(i) + "avg"
        ].min()
        out["KPI_SniffingPhase_Head" + str(i) + "_Pressure_max"] = df_SnPhase[
            "s_PressureHead" + str(i) + "avg"
        ].max()

        # start, end, duration
        out["KPI_SniffingPhase_Head" + str(i) + "_TimeStart"] = df_SnPhase.iloc[0]["Timestamp"]
        out["KPI_SniffingPhase_Head" + str(i) + "_AngleStart"] = df_SnPhase.iloc[0]["Angle"]

        out["KPI_SniffingPhase_Head" + str(i) + "_TimeEnd"] = df_SnPhase.iloc[-1]["Timestamp"]
        out["KPI_SniffingPhase_Head" + str(i) + "_AngleEnd"] = df_SnPhase.iloc[-1]["Angle"]

        out["KPI_SniffingPhase_Head" + str(i) + "_Time"] = (
            out["KPI_SniffingPhase_Head" + str(i) + "_TimeEnd"]
            - out["KPI_SniffingPhase_Head" + str(i) + "_TimeStart"]
        )
        out["KPI_SniffingPhase_Head" + str(i) + "_Angle"] = len(
            df_SnPhase
        )  # /10 ?? why not end-start?
        # fraction of full cycle
        out["KPI_SniffingPhase_Head" + str(i) + "_percentage"] = (
            out["KPI_SniffingPhase_Head" + str(i) + "_Angle"] / 3600 * 100
        )

        # SuctionPhase
        df_SuPhase = df_SnSuPhase[
            (df_SnSuPhase["s_PressureHead" + str(i)] > SnSuPhase_P_mean * 0.7)
            & (df_SnSuPhase["Angle"] < out["KPI_SniffingPhase_Head" + str(i) + "_AngleStart"])
        ]

        # basic statistics
        out["KPI_SuctionPhase_Head" + str(i) + "_Pressure_mean"] = statistics.mean(
            df_SuPhase["s_PressureHead" + str(i) + "avg"]
        )
        out["KPI_SuctionPhase_Head" + str(i) + "_Pressure_min"] = df_SuPhase[
            "s_PressureHead" + str(i) + "avg"
        ].min()
        out["KPI_SuctionPhase_Head" + str(i) + "_Pressure_max"] = df_SuPhase[
            "s_PressureHead" + str(i) + "avg"
        ].max()

        # start, end, duration
        out["KPI_SuctionPhase_Head" + str(i) + "_TimeStart"] = df_SuPhase.iloc[0]["Timestamp"]
        out["KPI_SuctionPhase_Head" + str(i) + "_AngleStart"] = df_SuPhase.iloc[0]["Angle"]

        out["KPI_SuctionPhase_Head" + str(i) + "_TimeEnd"] = df_SuPhase.iloc[-1]["Timestamp"]
        out["KPI_SuctionPhase_Head" + str(i) + "_AngleEnd"] = df_SuPhase.iloc[0]["Timestamp"]
        out["KPI_SuctionPhase_Head" + str(i) + "_AngleStart"] = df_SuPhase.iloc[0]["Angle"]

        out["KPI_SuctionPhase_Head" + str(i) + "_TimeEnd"] = df_SuPhase.iloc[-1]["Timestamp"]
        out["KPI_SuctionPhase_Head" + str(i) + "_AngleEnd"] = df_SuPhase.iloc[-1]["Angle"]

        out["KPI_SuctionPhase_Head" + str(i) + "_Time"] = (
            out["KPI_SuctionPhase_Head" + str(i) + "_TimeEnd"]
            - out["KPI_SuctionPhase_Head" + str(i) + "_TimeStart"]
        )
        out["KPI_SuctionPhase_Head" + str(i) + "_Angle"] = len(
            df_SuPhase
        )  # /10 ?? why not end-start?
        # fraction of full cycle
        out["KPI_SuctionPhase_Head" + str(i) + "_percentage"] = (
            out["KPI_SuctionPhase_Head" + str(i) + "_Angle"] / 3600 * 100
        )

    return out


def eval_full(df: pd.DataFrame) -> pd.DataFrame:
    out = dict()
    out["KPI_Cycle_TimeStart"] = df.iloc[0]["Timestamp"]
    out["KPI_Cycle_TimeEnd"] = df.iloc[-1]["Timestamp"]
    out["KPI_Cycle_Time"] = out["KPI_Cycle_TimeEnd"] - out["KPI_Cycle_TimeStart"]
    return out


def calc_KPIs(df: pd.DataFrame, servertime) -> pd.DataFrame:
    df1 = data_prep(df)
    out = eval_DPhase(df1)
    out.update(eval_SnSuPhase(df1))
    out.update(eval_full(df1))
    out.update(vibration_full(df1))
    out["servertime"] = servertime
    out["ID"] = 1
    return pd.DataFrame(data=out, index=[0])
