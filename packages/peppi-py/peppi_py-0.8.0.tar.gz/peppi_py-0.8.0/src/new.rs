use peppi::game::immutable::Game as PeppiGame;
use peppi::io::peppi::ser::Opts as PeppiWriteOpts;

fn from_py_via_json<'a, T: serde::Deserialize<'a>>(
	json: &Bound<PyModule>,
	d: Py<PyDict>,
) -> Result<T, PyO3ArrowError> {
	Ok(serde_json::from_str(
		&json
			.call_method1("dumps", (d,))?
			.extract::<String>()?)?)
}

fn _write_peppi(
	py: Python,
	path: String,
	game: Game,
	opts: PeppiWriteOpts,
) -> Result<Bound<Game>, PyO3ArrowError> {
	let pyarrow = py.import("pyarrow")?;
	let json = py.import("json")?;
	let game = PeppiGame {
		start: from_py_via_json(&json, game.start)?,
		end: from_py_via_json(&json, game.end)?,
		metadata: from_py_via_json(&json, game.metadata)?,
	};

	peppi::io::peppi::write(
		&mut io::BufWriter::new(fs::File::create(path)?),
		game,
		Some(&opts),
	)?;

	Ok(())
}

#[pyfunction]
#[pyo3(signature = (path))]
fn write_peppi(py: Python, path: String) -> PyResult<()> {
	_write_peppi(
		py,
		path,
		Default::default(),
	)
	.map_err(|e| PyOSError::new_err(e.to_string()))
}

