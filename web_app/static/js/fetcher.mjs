const submitForm = (url, formData, onSuccess, onError)=>{
  fetch(url,{
    method: 'POST',
    body: formData,
  })
    .then((response)=> {
      if (response.ok) {
        return response;
      }
      //throw response
      if (response.status === 633){
        throw response.json()
      }
      throw JSON.stringify({
        status: response.status,
        statusText: response.statusText
      });
    })
      .then(onSuccess)
      .catch(onError);
}

const getReference = (url, onSuccess, onError)=>{
  fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'text/html'
    },
  })
    .then((response)=>{
      if (response.ok){
        return response.json();
      }
      throw JSON.stringify({
        status: response.status,
        statusText: response.statusText
      });
    })
    .then(onSuccess)
    .catch(onError);
};


export {submitForm};
export {getReference};