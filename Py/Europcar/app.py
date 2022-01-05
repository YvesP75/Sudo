import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from stable_baselines3 import SAC

from rental_env import RentalEnv
from parameters import *



zz = np.load('zed.npy')
z = zz[0:10, 95:105, :10]
st.write(z)

nonzero = np.nonzero(z)
booking_day, car, rental_day = nonzero

car += 95

# Convert this grid to columnar data expected by Altair
source = pd.DataFrame({'booking_day': booking_day,
                       'car': car,
                       'rental_day': rental_day,
                       'value': zz[nonzero]})

st.write(source)

slider = alt.binding_range(min=0, max=9, step=1)
select_day = alt.selection_single(name="booking_day", fields=['booking_day'],
                                  bind=slider, init={'booking_day': 0})


c = alt.Chart(source).mark_rect().encode(
    x='rental_day:O',
    y='car:O',
    color='value:Q'
).properties(
    width=300,
    height=500
).add_selection(
    select_day
).transform_filter(
    select_day
)


st.altair_chart(c, use_container_width=True)
