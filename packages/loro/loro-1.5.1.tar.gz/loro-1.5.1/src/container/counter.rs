use crate::{doc::LoroDoc, err::PyLoroResult, value::ContainerID};
use loro::{ContainerTrait, LoroCounter as LoroCounterInner};
use pyo3::prelude::*;

#[pyclass(frozen)]
#[derive(Debug, Clone, Default)]
pub struct LoroCounter(pub LoroCounterInner);

#[pymethods]
impl LoroCounter {
    /// Create a new Counter.
    #[new]
    pub fn new() -> Self {
        Self::default()
    }

    /// Return container id of the Counter.
    #[getter]
    pub fn id(&self) -> ContainerID {
        self.0.id().into()
    }

    /// Increment the counter by the given value.
    pub fn increment(&self, py: Python, value: PyObject) -> PyLoroResult<()> {
        self.0.increment(value.extract::<f64>(py)?)?;
        Ok(())
    }

    /// Decrement the counter by the given value.
    pub fn decrement(&self, py: Python, value: PyObject) -> PyLoroResult<()> {
        self.0.decrement(value.extract::<f64>(py)?)?;
        Ok(())
    }

    /// Get the current value of the counter.
    #[getter]
    #[pyo3(name = "value")]
    pub fn get_value(&self) -> f64 {
        self.0.get_value()
    }

    pub fn doc(&self) -> Option<LoroDoc> {
        self.0.doc().map(|doc| doc.into())
    }
}
