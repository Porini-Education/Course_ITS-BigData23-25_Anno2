import streamlit as st
import requests
import os
import pandas as pd

function_app_url = os.getenv('function_app_url') or ''
function_app_code = os.getenv('function_app_code') or ''

def app():
    st.title('🎄Xmas Task Management🎄')

    col1, col2 = st.tabs(["Aggiungi Task", "Visualizza Task"])
    with col1:
        task = st.text_input('Nuovo task:')
        category = st.selectbox('Categoria:', ['General', 'Shopping', 'Food', 'Gifts'])
        priority = st.selectbox('Priorità:', ['Low', 'Normal', 'High'])

        if st.button('Aggiungi task'):
            response = requests.post(
                url=f'{function_app_url}/add_task',
                params= {
                    'code': function_app_code
                    },
                json={ 'task': task, 'category': category, 'priority': priority }
            )
            if response.status_code == 200:
                st.write(f'Task aggiunto: {task}')
    
    with col2:
        response = requests.get(
            url=f'{function_app_url}/get_tasks',
            params= {
                'code': function_app_code
                }
            )
        if response.status_code != 200:
            st.write('Errore nel recupero dei task')
            return
        tasks = response.json().get('tasks', [])
        task_df = pd.DataFrame(tasks)
        st.dataframe(task_df, use_container_width=True, hide_index=True)
        
                
        task_id = st.number_input('Task ID', min_value=1, )
        new_task_status = st.selectbox('Nuovo Stato:', ['Pending', 'Completed'])
        if st.button('Aggiorna Stato'):
            response = requests.post(
                    url=f'{function_app_url}/update_task',
                    params= {
                        'code': function_app_code
                        },
                    json={'id': task_id, 'status': new_task_status}
                )
            result = response.json()
            st.write(f"Status: {result['status']}, Task ID: {result['id']}, New Status: {result['new_status']}")

if __name__ == '__main__':
    app()